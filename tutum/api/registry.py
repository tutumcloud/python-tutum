from base import RESTModel


class Registry(RESTModel):
    """Represents a Tutum Registry object"""

    endpoint = "/registry"

    @property
    def pk(self):
        return getattr(self, 'host', None)