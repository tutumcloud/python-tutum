from http import send_request
from requests.auth import HTTPBasicAuth

def get_apikey(username, password):
    """
    Returns the user's apikey, or None if the credentials are invalid
    """
    auth = HTTPBasicAuth(username, password)
    json = send_request("GET", "/auth", auth=auth)
    apikey = None
    if json:
        objects = json.get('objects', None)
        if objects and len(objects) > 0:
            apikey = objects[0].get('key')
    return apikey