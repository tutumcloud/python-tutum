from __future__ import absolute_import
import urllib
import json
import websocket
import tutum
from .exceptions import TutumAuthError
from .base import StreamingAPI


class TutumEvents(StreamingAPI):
    def __init__(self):
        endpoint = "events"
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
            ws = websocket.WebSocketApp(self.url, header=self.header,
                                        on_open=self._on_open,
                                        on_message=self._on_message,
                                        on_error=self._on_error,
                                        on_close=self._on_close)
            ws.run_forever(ping_interval=5, ping_timeout=5, *args, **kwargs)
