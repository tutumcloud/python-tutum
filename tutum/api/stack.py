from .base import Mutable


class Stack(Mutable):
    """Represents a Tutum Stack object"""

    endpoint = "/stack"

    def start(self):
        """Starts the stack in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("start")

    def stop(self):
        """Stops the stack in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("stop")

    def redeploy(self):
        """Redeploy the stack in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        return self._perform_action("redeploy")

