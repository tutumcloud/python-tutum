from base import RESTModel


class Region(RESTModel):
    """Represents a Tutum region object"""

    endpoint = "/region"

    @classmethod
    def _pk_key(cls):
        return 'name'

    def delete(self):
        raise AttributeError("'delete' is not supported in 'Region'")

    def save(self):
        raise AttributeError("'save' is not supported in 'Region'")