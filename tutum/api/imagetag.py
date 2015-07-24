from .exceptions import TutumApiError
from .http import send_request
import tutum


class ImageTag(object):
    @classmethod
    def fetch(cls, name, tag):
        """Fetch ImageTag object by image name and tag

        :param name: name of the image
               tag: tag of the image
        :type name: str
              tag: str
        :returns: ImageTag object
        :raises: TutumApiError
        """
        instance = None
        detail_uri = tutum.rest_host.rstrip("/") + "/api/v1/image/%s/tag/%s/" % (name, tag)
        json = send_request('GET', detail_uri)
        if json:
            instance = cls()
            for k, v in list(json.items()):
                setattr(instance, k, v)
        return instance

    def get_all_attributes(self):
        """Returns a dict with all object attributes

        :returns: dict -- all object attributes as a dict
        """
        attributes = {}
        for attr in [attr for attr in vars(self) if not attr.startswith('_')]:
            attributes[attr] = getattr(self, attr, None)
        return attributes

    def build(self):
        """Build the image tag in Tutum.

        :returns: bool -- whether or not the operation succeeded
        :raises: TutumApiError
        """
        success = False
        if not getattr(self, "resource_uri", None):
            raise TutumApiError("You must fetch ImageTag object before building")
        url = tutum.rest_host.rstrip("/") + self.resource_uri.rstrip("/") + "/build/"
        json = send_request("POST", url)
        if json:
            for k, v in list(json.items()):
                setattr(self, k, v)
            success = True
        return success
