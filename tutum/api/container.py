from __future__ import absolute_import

from .base import Mutable, StreamingLog, Exec


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

    def redeploy(self, reuse_volumes=True):
        """Redeploy the container in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        params = {'reuse_volumes': reuse_volumes}
        return self._perform_action("redeploy", params=params)

    def logs(self, tail, follow, log_handler=StreamingLog.default_log_handler):
        """Follow logs for the container from Tutum streaming API

        :returns: None
        """
        logs = StreamingLog("container", self.pk, tail, follow)
        logs.on_message(log_handler)
        logs.run_forever()

    def execute(self, cmd, handler=Exec.default_message_handler):
        """Exec a command in the container via Tutum streaming API

        :param cmd: command to execute
        :return: None
        """
        if hasattr(self, "uuid"):
            exec_obj = Exec(self.uuid, cmd)
            exec_obj.on_message(handler)
            exec_obj.run_forever()
