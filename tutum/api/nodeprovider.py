from __future__ import absolute_import
from .base import Immutable


class Provider(Immutable):
    """Represents a Tutum Provider object"""

    endpoint = "/provider"

    @classmethod
    def _pk_key(cls):
        return 'name'

    def delete(self):
        raise AttributeError("'delete' is not supported in 'Provider'")

    def save(self):
        raise AttributeError("'save' is not supported in 'Provider'")
