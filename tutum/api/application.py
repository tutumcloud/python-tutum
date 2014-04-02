from base import RESTModel


class Application(RESTModel):

    endpoint = "/application"

    def start(self):
        return self._perform_action("start")

    def stop(self):
        return self._perform_action("stop")

    @property
    def logs(self):
        return self._expand_attribute("logs")