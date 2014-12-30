from .base import Immutable


class Action(Immutable):
    """Represents a Tutum Action object"""

    endpoint = "/action"

    @classmethod
    def _pk_key(cls):
        return 'uuid'