from base import Mutable, Taggable


class NodeCluster(Mutable, Taggable):
    """Represents a Tutum NodeCluster object"""

    endpoint = "/nodecluster"

    def deploy(self, tag=None):
        """Deploy the nodeCluster.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("deploy")