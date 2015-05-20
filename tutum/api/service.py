from .base import Mutable, Taggable, Triggerable, StreamingLog


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

    def logs(self, log_handler=StreamingLog.default_log_handler):
        """Follow logs for the service from Tutum streaming API

        :returns: None
        """
        logs = StreamingLog("service", self.pk)
        logs.on_message(log_handler)
        logs.run_forever()