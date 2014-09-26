from base import RESTModel


class NodeType(RESTModel):
    """Represents a Tutum nodetype object"""

    endpoint = "/nodetype"

    @classmethod
    def _pk_key(cls):
        return 'name'

    def delete(self):
        raise AttributeError("'delete' is not supported in 'NodeType'")

    def save(self):
        raise AttributeError("'save' is not supported in 'NodeType'")