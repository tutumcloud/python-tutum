import logging
from urlparse import urljoin

from requests import Request, Session

import tutum


class TutumServerError(Exception):
    pass


def send_request(method, path, **kwargs):
    json = None
    url  = urljoin(tutum.base_url, path.strip("/"))
    if not url.endswith("/"):
        url = "%s/" % url
    logging.info("%s %s %s" % (method, url, kwargs))
    # construct headers
    headers = {}
    headers['Content-Type']  = 'application/json'
    headers['User-Agent']    = 'python-tutum/v1.0'
    if tutum.user and tutum.apikey:
        headers['Authorization'] = 'ApiKey %s:%s' % (tutum.user, tutum.apikey)
    # construct request
    s = Session()
    req = Request(method, url, headers=headers, **kwargs)
    # make the request
    response = s.send(req.prepare())
    status_code = getattr(response, 'status_code', None)
    logging.info("Status: %s", str(status_code))
    # handle the response
    if not status_code:
        # Most likely network trouble
        raise TutumServerError("No Response (%s %s)" % (method, url))
    elif status_code >= 200 and status_code <= 299:
        # Success. Try to parse the response.
        try:
            json = response.json()
        except Exception as e:
            logging.error("Response: %s", response.text)
            raise TutumServerError("JSON Parse Error (%s %s)" % (method, url))
    else:
         # Server returned an error.
        logging.error("Response: %s", response.text)
        raise TutumServerError("Status %s (%s %s)" % (str(status_code), method, url))
    return json