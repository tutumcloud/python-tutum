import tutum
from requests import Request, Session
from urlparse import urljoin
from error import TutumErrorHTTP

BASE_URL = "https://app-test.tutum.co/api/v1/"

def send_request(method, path, **kwargs):
    json = None
    url  = urljoin(BASE_URL, path.strip("/"))
    try:
        # construct headers
        headers = {}
        headers['Content-Type']  = 'application/json'
        headers['User-Agent']    = 'python-tutum/v1.0'
        if tutum.user and tutum.apikey:
            headers['Authorization'] = 'ApiKey %s:%s' % (tutum.user, tutum.apikey)
        # construct request
        s = Session()
        req = Request('GET', url, headers=headers, **kwargs)
        # make the request
        response = s.send(req.prepare())
        status_code = getattr(response, 'status_code', None)
        # handle the response
        if status_code >= 200 and status_code <= 299:
            # Success.
            try:
                # Try to parse the response
                json = response.json()
            except Exception as e:
                raise TutumErrorHTTP("Error parsing JSON (%s)" % url)
        elif not status_code:
             # Most likely network trouble
            raise TutumErrorHTTP("No response (%s)" % url)
        elif status_code < 200 or status_code > 299:
             # Server returned an error
            raise TutumErrorHTTP("Recieved status %s (%s)" % (str(status_code), url))
    except Exception as e:
        print e
    return json