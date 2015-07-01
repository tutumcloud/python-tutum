from .base import Immutable


class AZ(Immutable):
    """Represents a Tutum Availability Zone object"""

    endpoint = "/az"

    @classmethod
    def _pk_key(cls):
        return 'name'
