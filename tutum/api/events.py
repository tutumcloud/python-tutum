import urllib
import websocket
import tutum
import json
from .exceptions import TutumAuthError

class TutumEvents:
    def __init__(self):
        if tutum.tutum_auth:
            endpoint = "events?auth=%s" % urllib.quote_plus(tutum.tutum_auth)
        else:
            endpoint = "events?user=%s&token=%s" % (tutum.user, tutum.apikey)
        url = "/".join([tutum.stream_url.rstrip("/"), endpoint.lstrip('/')])
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self._on_open,
                                         on_message=self._on_message,
                                         on_error=self._on_error,
                                         on_close=self._on_close)
        self.open_handler = None
        self.message_handler = None
        self.error_handler = None
        self.close_handler = None
        self.auth_error = False

    def _on_open(self, ws):
        if self.open_handler:
            self.open_handler()

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

    def _on_error(self, ws, error):
        if self.error_handler:
            self.error_handler(error)

    def _on_close(self, ws):
        if self.close_handler:
            self.close_handler()

    def on_open(self, handler):
        self.open_handler = handler

    def on_message(self, handler):
        self.message_handler = handler

    def on_error(self, handler):
        self.error_handler = handler

    def on_close(self, handler):
        self.close_handler = handler

    def run_forever(self):
        while True:
            if self.auth_error:
                raise TutumAuthError("Not authorized")
            self.ws.run_forever()
