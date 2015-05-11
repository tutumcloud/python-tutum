import json

from .base import Mutable


class Container(Mutable):
    """Represents a Tutum Container object"""

    endpoint = "/container"

    def save(self):
        raise AttributeError("'save' is not supported in 'Container' object. "
                             "Please use the related 'Service' object instead.")

    def start(self):
        """Starts the container in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("start")

    def stop(self):
        """Stops the container in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("stop")

    def redeploy(self, tag=None):
        """Redeploy the container in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("redeploy", data=json.dumps({"tag": tag}))

    @property
    def logs(self):
        """Fetches and returns the logs for the container from Tutum

        :returns: string -- the current logs of the container
        :raises: TutumApiError
        """
        return self._expand_attribute("logs")