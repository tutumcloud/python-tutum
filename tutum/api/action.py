from .base import Immutable, StreamingLog


class Action(Immutable):
    """Represents a Tutum Action object"""

    endpoint = "/action"

    @classmethod
    def _pk_key(cls):
        return 'uuid'

    def logs(self, tail, follow, log_handler=StreamingLog.default_log_handler):
        """Follow logs for the action from Tutum streaming API

        :returns: None
        """
        logs = StreamingLog("action", self.pk, tail, follow)
        logs.on_message(log_handler)
        logs.run_forever()
