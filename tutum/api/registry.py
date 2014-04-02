from base import RESTModel


class Registry(RESTModel):

    endpoint = "/registry"

    @property
    def pk(self):
        return getattr(self, 'host', None)