from base import RESTModel


class Image(RESTModel):
    """Represents a Tutum Image object"""

    endpoint = "/image"

    @property
    def pk(self):
        return getattr(self, 'name', None)