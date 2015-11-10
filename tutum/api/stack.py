from __future__ import absolute_import
from .base import Mutable
from .exceptions import TutumApiError
from .http import send_request


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

    def redeploy(self, reuse_volumes=True):
        """Redeploy the stack in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        params = {'reuse_volumes': reuse_volumes}
        return self._perform_action("redeploy", params=params)

    def export(self):
        """Export the stack in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        if not self._detail_uri:
            raise TutumApiError("You must save the object before performing this operation")
        url = "/".join([self._detail_uri, "export"])
        return send_request("GET", url, inject_header=False)
