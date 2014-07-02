from urlparse import urljoin

from requests import Request, Session

import tutum
from exceptions import TutumApiError, TutumAuthError


def send_request(method, path, **kwargs):
    json = None
    url = urljoin(tutum.base_url, path.strip("/"))
    if not url.endswith("/"):
        url = "%s/" % url
    tutum.logger.info("%s %s %s" % (method, url, kwargs))
    # construct headers
    headers = {'Content-Type': 'application/json', 'User-Agent': 'python-tutum/v1.0'}
    headers.update(tutum.auth.get_auth_header())
    # construct request
    s = Session()
    req = Request(method, url, headers=headers, **kwargs)
    # make the request
    response = s.send(req.prepare())
    status_code = getattr(response, 'status_code', None)
    tutum.logger.info("Status: %s", str(status_code))
    # handle the response
    if not status_code:
        # Most likely network trouble
        raise TutumApiError("No Response (%s %s)" % (method, url))
    elif 200 <= status_code <= 299:
        # Success
        if status_code != 204:
            # Try to parse the response.
            try:
                json = response.json()
            except Exception:
                raise TutumApiError("JSON Parse Error (%s %s). Response: %s" % (method, url, response.text))
        else:
            json = None
    else:
        # Server returned an error.
        if status_code == 401:
            raise TutumAuthError("Not authorized")
        else:
            raise TutumApiError("Status %s (%s %s). Response: %s" % (str(status_code), method, url, response.text))
    return json