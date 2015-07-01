from .base import Immutable


class NodeType(Immutable):
    """Represents a Tutum NodeType object"""

    endpoint = "/nodetype"

    @classmethod
    def _pk_key(cls):
        return 'name'
