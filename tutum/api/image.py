from base import RESTModel


class Image(RESTModel):
    """Represents a Tutum Image object"""

    endpoint = "/image"

    @classmethod
    def _pk_key(cls):
        return 'name'