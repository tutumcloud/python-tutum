from __future__ import absolute_import
from .base import Mutable, Taggable


class Image(Mutable, Taggable):
    """Represents a Tutum Image object"""

    endpoint = "/image"

    @classmethod
    def _pk_key(cls):
        return 'name'
