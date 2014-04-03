import json as json_parser

from http import send_request
from tutum.api.exceptions import TutumApiError


class RESTModel(object):
    _detail_uri = None

    def __init__(self, **kwargs):
        """
        Simply reflect all the values in kwargs.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, name, value):
        """
        Keep track of what attributes have been set.
        """
        current_value = getattr(self, name, None)
        if value != current_value:
            changed_attrs = self.__getchanges__()
            if not name in changed_attrs:
                changed_attrs.append(name)
                self.__setchanges__(changed_attrs)
        super(RESTModel, self).__setattr__(name, value)

    def __getchanges__(self):
        """
        Internal. Convenience method to get the changed attrs list.
        """
        return getattr(self, '__changedattrs__', [])

    def __setchanges__(self, val):
        """
        Internal. Convenience method to set the changed attrs list.
        """
        # Use the super implementation to prevent infinite recursion
        super(RESTModel, self).__setattr__('__changedattrs__', val)

    def _loaddict(self, dict):
        """
        Internal. Sets the model attributes to the dictionary values passed
        """
        endpoint = getattr(self, 'endpoint', None)
        assert endpoint, "Endpoint not specified for %s" % self.__class__.__name__
        for k, v in dict.items():
            setattr(self, k, v)
        self._detail_uri = "/".join([endpoint, self.pk])
        self.__setchanges__([])

    @property
    def pk(self):
        return getattr(self, 'uuid', None)

    @property
    def is_dirty(self):
        """
        Returns whether or not the model has unsaved changes.
        """
        return len(self.__getchanges__()) > 0

    @classmethod
    def list(cls):
        """
        List all models for the authenticated user.
        """
        containers = []
        endpoint = getattr(cls, 'endpoint', None)
        assert endpoint, "Endpoint not specified for %s" % cls.__name__
        json = send_request('GET', endpoint)
        if json:
            json_objects = json.get('objects', [])
            for json_obj in json_objects:
                instance = cls()
                instance._loaddict(json_obj)
                containers.append(instance)
        return containers

    @classmethod
    def fetch(cls, pk):
        """
        Fetch an individual model given the pk.
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

    def save(self):
        """
        Create or update the model in Tutum
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
            # Make the request
            success = False
            json = send_request(action, url, data=payload)
            if json:
                self._loaddict(json)
                success = True
        return success

    def refresh(self, force=False):
        """
        Reloads the model with remote information
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

    def delete(self):
        """
        Deletes the model in Tutum
        """
        success = False
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        action = "DELETE"
        url = self._detail_uri
        json = send_request(action, url)
        if json:
            self._loaddict(json)
            success = True
        return success

    def _perform_action(self, action):
        """
        Internal. Performs the specified action on the object remotely
        """
        success = False
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        url = "/".join([self._detail_uri, action])
        json = send_request("POST", url)
        if json:
            self._loaddict(json)
            success = True
        return success

    def _expand_attribute(self, attribute):
        """
        Internal. Expands the given attribute from remote information
        """
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        url = "/".join([self._detail_uri, attribute])
        json = send_request("GET", url)
        if json:
            return json[attribute]
        return None

    @classmethod
    def create(cls, **kwargs):
        """
        Returns a new instance of the model (without saving it)
        """
        return cls(**kwargs)