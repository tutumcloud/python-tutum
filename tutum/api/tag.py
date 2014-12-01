import json as json_parser

from base import Taggable
from http import send_request
from exceptions import TutumApiError


class Tag(object):
    def __init__(self):

        self.tags = []

    def add(self, tagname):
        """Add a tag to Tag object

        :returns:None
        """
        if isinstance(tagname, list):
            for t in tagname:
                self.tags.append({"name": t})
        else:
            self.tags.append({"name": tagname})

    @classmethod
    def create(cls, **kwargs):
        """Returns a new instance of the model (without saving it) with the attributes specified in ``kwargs``

        :returns: tag -- a new local instance of the Tag
        """
        return cls(**kwargs)

    def delete(self, tag):
        """Deletes the object in Tutum

        :returns: bool -- whether the operation was successful or not
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        if self.tags:
            raise TutumApiError("You must save the object before performing this operation")

        action = "DELETE"
        url = "/".join([self.endpoint, tag])
        send_request(action, url)
        if {"name": tag} in self.tags:
            self.tags.remove({"name": tag})

        return True

    @classmethod
    def fetch(cls, taggable):
        """"Fetch a tag object given the taggable object

        :param pk: the Taggable object (usually service, node, nodecluster, etc.)
        :type pk: Taggable
        :returns: Tag -- the instance fetched from Tutum
        :raises: TutumApiError
        """
        if not isinstance(taggable, Taggable):
            raise TutumApiError("The object does not support tag")
        if not taggable._detail_uri:
            raise TutumApiError("You must save the taggable object before performing this operation")
        tag = cls()

        tag.endpoint = "/".join([taggable._detail_uri, "tags"])
        tags = []
        for _tag in tag.list():
            tagname = _tag.get("name", "")
            if tagname:
                tags.append({"name": tagname})
        return tag

    def list(self, **kwargs):
        """List all tags of a taggable object, optionally filtered by ``kwargs``

        :returns: list -- a list of tags that match the query
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        objects=[]
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
        """Create or update the tag in Tutum

        :returns: bool -- whether the operation was successful or not
        """
        if not self.endpoint:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        json = send_request("POST", self.endpoint, data=json_parser.dumps(self.tags))
        if json:
            self.tags = []
            return True
        return False