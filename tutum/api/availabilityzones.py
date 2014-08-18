from base import RESTModel


class AZ(RESTModel):
    """Represents a Tutum availability zone object"""

    endpoint = "/az"

    @classmethod
    def _pk_key(cls):
        return 'resource_uri'