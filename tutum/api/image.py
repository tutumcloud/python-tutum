from base import RESTModel


class Image(RESTModel):

    endpoint = "/image"

    @property
    def pk(self):
        return getattr(self, 'name', None)