import json

from base import Mutable, Taggable, Webhookable


class Service(Mutable, Taggable, Webhookable):
    """Represents a Tutum Service object"""

    endpoint = "/service"

    def start(self):
        """Starts the service in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("start")

    def stop(self):
        """Stops the service in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("stop")

    def redeploy(self, tag=None):
        """Redeploy the service in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("redeploy", data=json.dumps({"tag": tag}))

    @property
    def logs(self):
        """Fetches and returns the logs for the service from Tutum

        :returns: string -- the current logs of the service
        :raises: TutumApiError
        """
        return self._expand_attribute("logs")