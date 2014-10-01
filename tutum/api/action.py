from base import RESTModel


class Action(RESTModel):
    """Represents a Tutum Action object"""

    endpoint = "/action"

    @classmethod
    def _pk_key(cls):
        return 'uuid'

    def delete(self):
        raise AttributeError("'delete' is not supported in 'Action'")

    def save(self):
        raise AttributeError("'save' is not supported in 'Action'")