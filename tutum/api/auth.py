import ConfigParser
import os
from requests.auth import HTTPBasicAuth

import tutum
from http import send_request


def authenticate(username, password):
    """
    Authenticates a Tutum user
    """
    success = False
    apikey = get_apikey(username, password)
    if apikey:
        success = True
        tutum.user = username
        tutum.apikey = apikey
    return success


def get_apikey(username, password):
    """
    Returns the user's apikey, or None if username/password incorrect
    """
    auth = HTTPBasicAuth(username, password)
    json = send_request("GET", "/auth", auth=auth)
    apikey = None
    if json:
        objects = json.get('objects', None)
        if objects and len(objects) > 0:
            apikey = objects[0].get('key')
    return apikey


def is_authenticated():
    """
    Returns whether the tutum user and apikey is set
    """
    return tutum.user != None and tutum.apikey != None


def logout():
    """
    Sets the tutum user and apikey to None
    """
    tutum.user = None
    tutum.apikey = None


def load_from_file(file="~/.tutum"):
    """
    Attempts to read tutum's credentials from a config file and return a tuple of (user,apikey)
    """
    try:
        cfgfile = os.path.expanduser(file)
        cp = ConfigParser.ConfigParser()
        cp.read(cfgfile)
        return (cp.get("auth", "user"), cp.get("auth", "apikey"))
    except ConfigParser.Error:
        return (None, None)