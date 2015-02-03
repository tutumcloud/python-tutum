from .base import Immutable


class Volume(Immutable):
    """Represents a Tutum Volume object"""

    endpoint = "/volume"

    @classmethod
    def _pk_key(cls):
        return 'uuid'