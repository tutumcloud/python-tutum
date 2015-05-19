from .base import Mutable, Taggable, Triggerable


class Service(Mutable, Taggable, Triggerable):
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

    def redeploy(self):
        """Redeploy the service in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("redeploy")

    def scale(self):
        """Scale the service in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("scale")

    @property
    def logs(self):
        """Fetches and returns the logs for the service from Tutum

        :returns: string -- the current logs of the service
        :raises: TutumApiError
        """
        return self._expand_attribute("logs")