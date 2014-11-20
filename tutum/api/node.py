from base import Mutable, Taggable


class Node(Mutable, Taggable):
    """Represents a Tutum Node object"""

    endpoint = "/node"

    def save(self):
        raise AttributeError("'save' is not supported in 'Node'")

    def deploy(self, tag=None):
        """Deploy the nodeCluster.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("deploy")