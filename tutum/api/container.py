import json

from .base import Mutable, StreamingLog


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

    def logs(self, tail, follow, log_handler=StreamingLog.default_log_handler):
        """Follow logs for the container from Tutum streaming API

        :returns: None
        """
        logs = StreamingLog("container", self.pk, tail, follow)
        logs.on_message(log_handler)
        logs.run_forever()
