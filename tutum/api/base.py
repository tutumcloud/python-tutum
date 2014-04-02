import json as json_parser

from http import send_request


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
        if not endpoint:
            raise Exception("Endpoint not specified for %s" % cls.__name__)
        json = send_request('GET', endpoint)
        if json:
            json_objects = json.get('objects', [])
            for json_obj in json_objects:
                instance = cls(**json_obj)
                instance.__setchanges__([])
                containers.append(instance)
        return containers

    @classmethod
    def fetch(cls, pk):
        """
        Fetch an individual model given the pk.
        """
        instance = None
        endpoint = getattr(cls, 'endpoint', None)
        if not endpoint:
            raise Exception("Endpoint not specified for %s" % cls.__name__)
        detail_uri = "/".join([endpoint, pk])
        json = send_request('GET', detail_uri)
        if json:
            instance = cls(**json)
            instance._detail_uri = detail_uri
            instance.__setchanges__([])
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
            cls      = self.__class__
            endpoint = getattr(cls, 'endpoint', None)
            if not endpoint:
                raise Exception("Endpoint not specified for %s" % cls.__name__)
            # Figure out whether we should do a create or update
            action   = None
            url      = None
            if not self._detail_uri:
                action  = "POST"
                url     = endpoint
            else:
                action  = "PATCH"
                url     = self._detail_uri
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
            json    = send_request(action, url, data=payload)
            if json:
                for k, v in json.items():
                    setattr(self, k, v)
                self.__setchanges__([])
                success = True
        return success

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)