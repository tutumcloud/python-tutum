import json as json_parser

from http import send_request
from exceptions import TutumApiError


class Restful(object):
    _detail_uri = None

    def __init__(self, **kwargs):
        """Simply reflect all the values in kwargs"""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, name, value):
        """Keeps track of what attributes have been set"""
        current_value = getattr(self, name, None)
        if value != current_value:
            changed_attrs = self.__getchanges__()
            if not name in changed_attrs:
                changed_attrs.append(name)
                self.__setchanges__(changed_attrs)
        super(Restful, self).__setattr__(name, value)

    def __getchanges__(self):
        """Internal. Convenience method to get the changed attrs list"""
        return getattr(self, '__changedattrs__', [])

    def __setchanges__(self, val):
        """Internal. Convenience method to set the changed attrs list"""
        # Use the super implementation to prevent infinite recursion
        super(Restful, self).__setattr__('__changedattrs__', val)

    def _loaddict(self, dict):
        """Internal. Sets the model attributes to the dictionary values passed"""
        endpoint = getattr(self, 'endpoint', None)
        assert endpoint, "Endpoint not specified for %s" % self.__class__.__name__
        for k, v in dict.items():
            setattr(self, k, v)
        self._detail_uri = "/".join([endpoint, self.pk])
        self.__setchanges__([])

    @property
    def pk(self):
        """Returns the primary key for the object.

        :returns: str -- the primary key for the object
        """
        return getattr(self, self._pk_key(), None)

    @classmethod
    def _pk_key(cls):
        """Internal. Returns the attribute name that acts as primary key of the model. Can be overridden by subclasses.

        :returns: str -- the name of the primary key attribute for the model
        """
        return 'uuid'

    @property
    def is_dirty(self):
        """Returns whether or not the object has unsaved changes

        :returns: bool -- whether or not the object has unsaved changes
        """
        return len(self.__getchanges__()) > 0

    def _perform_action(self, action, data={}):
        """Internal. Performs the specified action on the object remotely"""
        success = False
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        url = "/".join([self._detail_uri, action])
        json = send_request("POST", url, data=data)
        if json:
            self._loaddict(json)
            success = True
        return success

    def _expand_attribute(self, attribute):
        """Internal. Expands the given attribute from remote information"""
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        url = "/".join([self._detail_uri, attribute])
        json = send_request("GET", url)
        if json:
            return json[attribute]
        return None

    def get_all_attributes(self):
        """Returns a dict with all object attributes

        :returns: dict -- all object attributes as a dict
        """
        attributes = {}
        for attr in [attr for attr in vars(self) if not attr.startswith('_')]:
            attributes[attr] = getattr(self, attr, None)
        return attributes


class Immutable(Restful):
    @classmethod
    def fetch(cls, pk):
        """Fetch an individual model given the pk

        :param pk: The primary key for the object (usually UUID)
        :type pk: str
        :returns: RESTModel -- the instance fetched from Tutum
        :raises: TutumApiError
        """
        instance = None
        endpoint = getattr(cls, 'endpoint', None)
        assert endpoint, "Endpoint not specified for %s" % cls.__name__
        detail_uri = "/".join([endpoint, pk])
        json = send_request('GET', detail_uri)
        if json:
            instance = cls()
            instance._loaddict(json)
        return instance

    @classmethod
    def list(cls, **kwargs):
        """List all objects for the authenticated user, optionally filtered by ``kwargs``

        :returns: list -- a list of objects that match the query
        """
        objects = []
        endpoint = getattr(cls, 'endpoint', None)
        assert endpoint, "Endpoint not specified for %s" % cls.__name__

        json = send_request('GET', endpoint, params=kwargs)
        if json:
            json_objects = json.get('objects', [])
            for json_obj in json_objects:
                instance = cls()
                instance._loaddict(json_obj)
                objects.append(instance)
        return objects

    def refresh(self, force=False):
        """Reloads the object with remote information

        :param force: Force reloading even if there are pending changes
        :type force: bool
        :returns: bool -- whether the operation was successful or not
        """
        success = False
        if self.is_dirty and not force:
            # We have local non-committed changes - rejecting the refresh
            success = False
        elif not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        else:
            json = send_request("GET", self._detail_uri)
            if json:
                self._loaddict(json)
                success = True
        return success


class Mutable(Immutable):
    @classmethod
    def create(cls, **kwargs):
        """Returns a new instance of the model (without saving it) with the attributes specified in ``kwargs``

        :returns: RESTModel -- a new local instance of the model
        """
        return cls(**kwargs)

    def delete(self, suffix=""):
        """Deletes the object in Tutum

        :param suffix: delete affiliated stuff attached the object, like tags etc.
        :type suffix: string
        :returns: bool -- whether the operation was successful or not
        """
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        action = "DELETE"
        url = self._detail_uri
        if suffix:
            if suffix.startswith("/"):
                suffix = suffix[1:]
            if url.endswith("/"):
                url = "".join([url, suffix])
            else:
                url = "/".join([url, suffix])
        json = send_request(action, url)
        if json:
            self._loaddict(json)
        else:
            # Object deleted successfully and nothing came back - deleting PK reference.
            self._detail_uri = None
            # setattr(self, self._pk_key(), None) -- doesn't work
            self.__setchanges__([])
        return True

    def save(self):
        """Create or update the model in Tutum

        :returns: bool -- whether the operation was successful or not
        """
        success = False
        if not self.is_dirty:
            # No changes
            success = True
        else:
            cls = self.__class__
            endpoint = getattr(cls, 'endpoint', None)
            assert endpoint, "Endpoint not specified for %s" % self.__class__.__name__
            # Figure out whether we should do a create or update
            if not self._detail_uri:
                action = "POST"
                url = endpoint
            else:
                action = "PATCH"
                url = self._detail_uri
            # Construct the necessary params
            params = {}
            for attr in self.__getchanges__():
                value = getattr(self, attr, None)
                if value:
                    params[attr] = value
            # Construct the json body
            payload = None
            if params:
                payload = json_parser.dumps(params)
            if not payload:
                payload = json_parser.dumps({})
            # Make the request
            success = False
            json = send_request(action, url, data=payload)
            if json:
                self._loaddict(json)
                success = True
        return success


class Taggable(Restful):
    class Tag(object):
        def __init__(self, restful):
            self.restful = restful

        def add(self, tag):
            return self.restful._tag_add(tag)

        def delete(self, tag):
            return self.restful._tag_delete(tag)

        def list(self):
            return self.restful._tag_list()

    @property
    def tag(self):
        return Taggable.Tag(self)

    def _tag_add(self, tag):
        """Adds a tag from a taggable object

        :param tag: the tag name to be added
        :type tag: string
        :returns: bool -- whether the operation was successful or not
        """
        return self._perform_action('tags', data=json_parser.dumps({"name": tag}))

    def _tag_delete(self, tag):
        """Deletes a tag from a taggable object

        :param tag: the tag name to be deleted
        :type tag: string
        :returns: bool -- whether the operation was successful or not
        """
        return self.delete("tags/%s" % tag)

    def _tag_list(self):
        """List all tags for the taggable objects

        :returns: list -- a list of tags that match the query
        """
        url = "/".join([self._detail_uri, "tags"])
        json = send_request('GET', url)
        if json:
            return json.get('objects', [])
        return []