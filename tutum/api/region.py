from base import RESTModel


class Region(RESTModel):
    """Represents a Tutum region object"""

    endpoint = "/region"

    @classmethod
    def _pk_key(cls):
        return 'resource_uri'