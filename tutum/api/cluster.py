import json

from base import RESTModel


class Cluster(RESTModel):
    """Represents a Tutum Cluster object"""

    endpoint = "/application"

    def start(self):
        """Starts the cluster in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("start")

    def stop(self):
        """Stops the cluster in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("stop")

    def redeploy(self, tag=None):
        """Redeploy the cluster in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("redeploy", data=json.dumps({"tag": tag}))

    @property
    def logs(self):
        """Fetches and returns the logs for the cluster from Tutum

        :returns: string -- the current logs of the cluster
        :raises: TutumApiError
        """
        return self._expand_attribute("logs")