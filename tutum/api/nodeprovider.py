from base import RESTModel


class Provider(RESTModel):
    """Represents a Tutum Provider object"""

    endpoint = "/provider"

    @classmethod
    def _pk_key(cls):
        return 'name'

    def delete(self):
        raise AttributeError("'delete' is not supported in 'Provider'")

    def save(self):
        raise AttributeError("'save' is not supported in 'Provider'")