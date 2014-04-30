from base import RESTModel


class Application(RESTModel):
    """Represents a Tutum Application object"""

    endpoint = "/application"

    def start(self):
        """Starts the application in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("start")

    def stop(self):
        """Stops the application in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("stop")

    def redeploy(self, tag=None):
        """Redeploy the application in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("redeploy", data={"tag": tag})

    @property
    def logs(self):
        """Fetches and returns the logs for the application from Tutum

        :returns: string -- the current logs of the application
        :raises: TutumApiError
        """
        return self._expand_attribute("logs")