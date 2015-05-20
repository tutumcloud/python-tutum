import urllib
import json

import tutum
from .exceptions import TutumAuthError
from .base import StreamingAPI


class TutumEvents(StreamingAPI):
    def __init__(self):
        if tutum.tutum_auth:
            endpoint = "events?auth=%s" % urllib.quote_plus(tutum.tutum_auth)
        else:
            endpoint = "events?user=%s&token=%s" % (tutum.user, tutum.apikey)
        super(self.__class__, self).__init__(endpoint)

    def _on_message(self, ws, message):
        try:
            event = json.loads(message)
        except ValueError:
            return

        if event.get("type") == "error" and event.get("data", {}).get("errorMessage") == "UNAUTHORIZED":
            self.auth_error = True
            raise TutumAuthError("Not authorized")
        if event.get("type") == "auth":
            return

        if self.message_handler:
            self.message_handler(event)

    def run_forever(self, *args, **kwargs):
        while True:
            if self.auth_error:
                raise TutumAuthError("Not authorized")
            self.ws.run_forever(*args, **kwargs)
