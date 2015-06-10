from .base import Taggable
from .exceptions import TutumApiError


class Tag(object):
    def __init__(self):
        self.tags = []

    def add(self, tagname):
        """Add a tag or a list of tags to Tag object. This operation will not take effect unless save() is called.

        :returns:None
        """

        if isinstance(tagname, list):
            for t in tagname:
                self.taggable.tags.append({"name": t})
        else:
            self.taggable.tags.append({"name": tagname})

        self.taggable.__addchanges__('tags')

    @classmethod
    def create(cls, **kwargs):
        """Returns a new instance of the model (without saving it) with the attributes specified in ``kwargs``

        :returns: tag -- a new local instance of the Tag
        """
        return cls(**kwargs)

    def remove(self, tagname):
        """remove a tag or a list of tags from Tutum. This operation will not take effect unless save() is called.

        :returns: bool -- whether the operation was successful or not
        """
        if not self.taggable:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        _tags = []
        tagnames = []
        if isinstance(tagname, list):
            for n in tagname:
                tagnames.append(n)
        else:
            tagnames.append(tagname)

        for t in self.taggable.tags:
            for tagname in tagnames:
                if t.get("name", "") == tagname:
                    _tags.append(t)

        if _tags:
            for _tag in _tags:
                self.taggable.tags.remove(_tag)
            self.taggable.__addchanges__('tags')

    def delete(self, tagname):
        """delete a tag or a list of tags from Tutum.

        :returns: bool -- whether the operation was successful or not
        """
        if not self.taggable:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        if self.taggable.is_dirty:
            raise TutumApiError("You must save the tab object before performing this operation")

        self.remove(tagname)
        return self.save()

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
        tag.taggable = taggable

        return tag

    def list(self, **kwargs):
        """List all tags of a taggable object, optionally filtered by ``kwargs``

        :returns: list -- a list of tags that match the query
        """
        if not self.taggable:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        return self.taggable.tags

    def save(self):
        """Create or update the tag in Tutum

        :returns: bool -- whether the operation was successful or not
        """
        if not self.taggable:
            raise TutumApiError("You must initialize the tag object before performing this operation")

        return self.taggable.save()
