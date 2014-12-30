import json as json_parser

from .base import Webhookable
from .http import send_request
from .exceptions import TutumApiError


class WebhookHandler(object):
    def __init__(self):
        self.webhookhandlers = []

    def add(self, handler):
        """Add a hander to WebhookHandler object

        :returns:None
        """
        if isinstance(handler, list):
            for h in handler:
                self.webhookhandlers.append({"name": h})
        else:
            self.webhookhandlers.append({"name": handler})

    @classmethod
    def create(cls, **kwargs):
        """Returns a new instance of the model (without saving it) with the attributes specified in ``kwargs``

        :returns: webhookhandler -- a new local instance of the WebhookHandler
        """
        return cls(**kwargs)

    def delete(self, handler):
        """Deletes the object in Tutum

        :returns: bool -- whether the operation was successful or not
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the WebhookHandler object before performing this operation")

        if self.webhookhandlers:
            raise TutumApiError("You must save the object before performing this operation")

        action = "DELETE"
        url = "/".join([self.endpoint, handler])
        send_request(action, url)
        if {"name": handler} in self.webhookhandlers:
            self.webhookhandlers.remove({"name": handler})
        return True

    @classmethod
    def fetch(cls, webhookable):
        """"Fetch a Webhandler object given the Webhookable object

        :param pk: the Taggable object (usually service, node, nodecluster, etc.)
        :type pk: Taggable
        :returns: Tag -- the instance fetched from Tutum
        :raises: TutumApiError
        """
        if not isinstance(webhookable, Webhookable):
            raise TutumApiError("The object does not support web hook")
        if not webhookable._detail_uri:
            raise TutumApiError("You must save the webhookable object before performing this operation")
        webhookhandler = cls()
        webhookhandler.endpoint = "/".join([webhookable._detail_uri, "webhook/handler"])
        handlers = []
        for handler in webhookhandler.list():
            handlername = handler.get("name", "")
            if handlername:
                handlers.append({"name": handlername})
        return webhookhandler

    def list(self, **kwargs):
        """List all handlers from a webhookable object, optionally filtered by ``kwargs``

        :returns: list -- a list of webhook handlers that match the query
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the WebhookHander object before performing this operation")

        objects = []
        while True:
            json = send_request('GET', self.endpoint, params=kwargs)
            objs = json.get('objects', [])
            meta = json.get('meta', {})
            next_url = meta.get('next', '')
            offset = meta.get('offset', 0)
            limit = meta.get('limit', 0)
            objects.extend(objs)
            if next_url:
                kwargs['offset'] = offset + limit
                kwargs['limit'] = limit
            else:
                break

        return objects

    def save(self):
        """Create or update the webhandler in Tutum

        :returns: bool -- whether the operation was successful or not
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the WebhookHander object before performing this operation")

        json = send_request("POST", self.endpoint, data=json_parser.dumps(self.webhookhandlers))
        if json:
            self.webhookhandlers = []
            return True
        return False

    def call(self, uuid):
        """Call the webhook handler given the uuid

        :returns: bool -- whether the operation was successful or not
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the WebhookHander object before performing this operation")

        json = send_request("POST", "/".join([self.endpoint, uuid + "/call"]))
        if json:
            return True
        return False