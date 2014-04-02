from base import RESTModel


class Role(RESTModel):

    endpoint = "/role"

    @property
    def pk(self):
        return getattr(self, 'scope', None)