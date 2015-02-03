from .base import Immutable


class VolumeGroup(Immutable):
    """Represents a Tutum VolumeGroup object"""

    endpoint = "/volumegroup"

    @classmethod
    def _pk_key(cls):
        return 'uuid'