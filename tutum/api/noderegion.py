from .base import Immutable


class Region(Immutable):
    """Represents a Tutum Region object"""

    endpoint = "/region"

    @classmethod
    def _pk_key(cls):
        return 'name'
