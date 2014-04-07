from base import RESTModel


class Container(RESTModel):
    """Represents a Tutum Container object"""

    endpoint = "/container"

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

    @property
    def logs(self):
        """Fetches and returns the logs for the container from Tutum

        :returns: string -- the current logs of the container
        :raises: TutumApiError
        """
        return self._expand_attribute("logs")