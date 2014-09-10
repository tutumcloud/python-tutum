from base import RESTModel


class Provider(RESTModel):
    """Represents a Tutum nodecluster object"""

    endpoint = "/provider"

    @classmethod
    def _pk_key(cls):
        return 'name'