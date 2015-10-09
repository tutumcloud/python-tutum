from __future__ import absolute_import
from requests import Request, Session
from requests import utils

from urllib.parse import urljoin
import tutum
from .exceptions import TutumApiError, TutumAuthError


def send_request(method, path, inject_header=True, **kwargs):
    json = None
    url = urljoin(tutum.base_url, path.strip("/"))
    if not url.endswith("/"):
        url = "%s/" % url
    user_agent = 'python-tutum/%s' % tutum.__version__
    if tutum.user_agent:
        user_agent = "%s %s" % (tutum.user_agent, user_agent)
    # construct headers
    headers = {'Content-Type': 'application/json', 'User-Agent': user_agent}
    headers.update(tutum.auth.get_auth_header())
    tutum.logger.info("Request: %s %s %s %s" % (method, url, headers, kwargs))
    # construct request
    s = Session()
    req = Request(method, url, headers=headers, **kwargs)
    # get environment proxies
    env_proxies = utils.get_environ_proxies(url) or {}
    kw_args = {'proxies': env_proxies}
    # make the request
    response = s.send(req.prepare(), **kw_args)
    status_code = getattr(response, 'status_code', None)
    tutum.logger.info("Response: Status %s" % str(status_code))
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
                if response.headers and inject_header:
                    json["tutum_action_uri"] = response.headers.get("X-Tutum-Action-URI", "")
            except TypeError:
                raise TutumApiError("JSON Parse Error (%s %s). Response: %s" % (method, url, response.text))
        else:
            json = None
    else:
        # Server returned an error.
        if status_code == 401:
            raise TutumAuthError("Not authorized")
        else:
            raise TutumApiError("Status %s (%s %s). Response: %s" % (str(status_code), method, url, response.text))
    tutum.logger.info("Response: %s" % json)
    return json
