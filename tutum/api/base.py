from http import send_request
from urlparse import urljoin

class RESTModel(object):

    def __init__(self, **kwargs):
        """
        Simply reflect all the values in kwargs.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

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
                containers.append(cls(**json_obj))
        return containers

    @classmethod
    def fetch(cls, uuid):
        """
        Fetch an individual model given the uuid.
        """
        instance = None
        endpoint = getattr(cls, 'endpoint', None)
        if not endpoint:
            raise Exception("Endpoint not specified for %s" % cls.__name__)
        json = send_request('GET', "/".join([endpoint, uuid]))
        if json:
            instance = cls(**json)
        return instance

    def save(self):
        """
        Create or update a model.
        """
        cls      = self.__class__
        endpoint = getattr(cls, 'endpoint', None)
        if not endpoint:
            raise Exception("Endpoint not specified for %s" % cls.__name__)
        # Figure out whether we should do a create or update
        uuid     = getattr(self, 'uuid', None)
        action   = None
        url      = None
        attrs    = None
        if not uuid:
            action  = "POST"
            url     = endpoint
            attrs   = getattr(cls, 'params_for_create', None)
        else:
            action  = "PUT"
            url     = "/".join([endpoint, uuid])
            attrs   = getattr(cls, 'params_for_update', None)
        if not attrs:
            raise Exception("Don't know how to %s %s object." % (action, cls.__name__))
        # Construct the necessary params
        params = {}
        for attr in attrs:
            value = getattr(self, attr, None)
            if value:
                params[attr] = value
        # Make the request
        success = False
        json    = send_request(action, url, params=params)
        if json:
            for k, v in json.items():
                setattr(self, k, v)
            success = True
        return success
