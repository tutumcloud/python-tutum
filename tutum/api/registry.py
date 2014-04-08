from base import RESTModel


class Registry(RESTModel):
    """Represents a Tutum Registry object"""

    endpoint = "/registry"

    @classmethod
    def _pk_key(cls):
        return 'host'