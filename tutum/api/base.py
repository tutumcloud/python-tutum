from __future__ import absolute_import
import json as json_parser
import urllib
import logging

import websocket

import tutum
from .http import send_request
from .exceptions import TutumApiError, TutumAuthError

logger = logging.getLogger("python-tutum")


class Restful(object):
    _detail_uri = None

    def __init__(self, **kwargs):
        """Simply reflect all the values in kwargs"""
        for k, v in list(kwargs.items()):
            setattr(self, k, v)

    def __addchanges__(self, name):
        changed_attrs = self.__getchanges__()
        if not name in changed_attrs:
            changed_attrs.append(name)
            self.__setchanges__(changed_attrs)

    def __setattr__(self, name, value):
        """Keeps track of what attributes have been set"""
        current_value = getattr(self, name, None)
        if value != current_value:
            self.__addchanges__(name)
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
        for k, v in list(dict.items()):
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
    def list(cls, limit=None, **kwargs):
        """List all objects for the authenticated user, optionally filtered by ``kwargs``

        :returns: list -- a list of objects that match the query
        """
        restful = []
        endpoint = getattr(cls, 'endpoint', None)
        assert endpoint, "Endpoint not specified for %s" % cls.__name__

        objects = []
        while True:
            if limit and len(objects) >= limit:
                break
            json = send_request('GET', endpoint, params=kwargs)
            objs = json.get('objects', [])
            meta = json.get('meta', {})
            next_url = meta.get('next', '')
            offset = meta.get('offset', 0)
            api_limit = meta.get('limit', 0)
            objects.extend(objs)
            if next_url:
                kwargs['offset'] = offset + api_limit
                kwargs['limit'] = api_limit
            else:
                break
        if limit:
            objects = objects[:limit]
        for obj in objects:
            instance = cls()
            instance._loaddict(obj)
            restful.append(instance)
        return restful

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

    def delete(self):
        """Deletes the object in Tutum
        :returns: bool -- whether the operation was successful or not
        """
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        action = "DELETE"
        url = self._detail_uri
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


class Taggable(object):
    pass


class Triggerable(object):
    pass


class StreamingAPI(object):
    def __init__(self, endpoint):
        self._ws_init(endpoint)

    def _ws_init(self, endpoint):
        self.url = "/".join([tutum.stream_url.rstrip("/"), endpoint.lstrip('/')])

        user_agent = 'python-tutum/%s' % tutum.__version__
        if tutum.user_agent:
            user_agent = "%s %s" % (tutum.user_agent, user_agent)
        self.header = {'User-Agent': user_agent}
        logger.info("websocket: %s %s" % (self.url, self.header))
        self.open_handler = None
        self.message_handler = None
        self.error_handler = None
        self.close_handler = None
        self.auth_error = False

    def _on_open(self, ws):
        if self.open_handler:
            self.open_handler()

    def _on_message(self, ws, message):
        if self.message_handler:
            self.message_handler(message)

    def _on_error(self, ws, error):
        if self.error_handler:
            self.error_handler(error)

    def _on_close(self, ws):
        if self.close_handler:
            self.close_handler()

    def on_open(self, handler):
        self.open_handler = handler

    def on_message(self, handler):
        self.message_handler = handler

    def on_error(self, handler):
        self.error_handler = handler

    def on_close(self, handler):
        self.close_handler = handler

    def run_forever(self, *args, **kwargs):
        while True:
            if getattr(self, "auth_error", False):
                raise TutumAuthError("Not authorized")
            ws = websocket.WebSocketApp(self.url, header=self.header,
                                        on_open=self._on_open,
                                        on_message=self._on_message,
                                        on_error=self._on_error,
                                        on_close=self._on_close)
            ws.run_forever(ping_interval=5, ping_timeout=5, *args, **kwargs)


class StreamingLog(StreamingAPI):
    def __init__(self, obj_type, uuid, tail, follow):
        if tutum.tutum_auth:
            endpoint = "%s/%s/logs/?auth=%s" % (obj_type, uuid, urllib.quote_plus(tutum.tutum_auth))
        else:
            endpoint = "%s/%s/logs/?user=%s&token=%s" % (obj_type, uuid, tutum.user, tutum.apikey)
        if tail:
            endpoint = "%s&tail=%d" % (endpoint, tail)
        if not follow:
            endpoint = "%s&follow=%s" % (endpoint, str(follow).lower())

        super(self.__class__, self).__init__(endpoint)

    @staticmethod
    def default_log_handler(message):
        print message

    def run_forever(self, *args, **kwargs):
        ws = websocket.WebSocketApp(self.url, header=self.header,
                                    on_open=self._on_open,
                                    on_message=self._on_message,
                                    on_error=self._on_error,
                                    on_close=self._on_close)
        ws.run_forever(ping_interval=5, ping_timeout=5, *args, **kwargs)
