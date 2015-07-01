from .base import Mutable, Taggable
from tutum.api.nodetype import NodeType
from tutum.api.noderegion import Region


class NodeCluster(Mutable, Taggable):
    """Represents a Tutum NodeCluster object"""

    endpoint = "/nodecluster"

    def deploy(self, tag=None):
        """Deploy the nodeCluster.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("deploy")

    @classmethod
    def create(cls, **kwargs):
        for key, value in kwargs.items():
            if key == "node_type" and isinstance(value, NodeType):
                kwargs[key] = getattr(value, "resource_uri", "")
            if key == "region" and isinstance(value, Region):
                kwargs[key] = getattr(value, "resource_uri", "")
        return cls(**kwargs)

    def upgrade_docker(self):
        """upgrade docker on the nodeCluster.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("docker-upgrade")
