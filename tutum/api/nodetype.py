from base import RESTModel


class NodeType(RESTModel):
    """Represents a Tutum nodetype object"""

    endpoint = "/nodetype"

    @classmethod
    def _pk_key(cls):
        return 'name'