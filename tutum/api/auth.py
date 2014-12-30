import configparser
import os

from requests.auth import HTTPBasicAuth
import tutum
from .http import send_request


def authenticate(username, password):
    """Authenticates a Tutum user using username and password. If successful, automatically sets ``tutum.user`` and ``tutum.apikey``

    :param username: The username of the user to authenticate
    :type username: str.
    :param password: The password of the user to authenticate
    :type password: str.
    :raises: TutumAuthError
    """
    user, apikey = get_auth(username, password)
    if user:
        tutum.user = user
    if apikey:
        tutum.apikey = apikey


def get_auth(username, password):
    """Returns the user's Username and ApiKey, or raises an exception if username/password incorrect

    :param username: The username/email of the user to authenticate
    :type username: str
    :param password: The password of the user to authenticate
    :type password: str
    :raises: TutumAuthError
    :returns: str, str -- the Username, ApiKey to use for the given username/email
    """
    auth = HTTPBasicAuth(username, password)
    json = send_request("GET", "/auth", auth=auth)
    user = username
    apikey = None
    if json:
        objects = json.get('objects', None)
        if objects and len(objects) > 0:
            user = objects[0].get('username', username)
            apikey = objects[0].get('key')
    return user, apikey


def is_authenticated():
    """Returns whether the tutum user and apikey are set

    :returns: bool -- whether the tutum user and apikey are set
    """
    return tutum.user != None and tutum.apikey != None


def logout():
    """Sets the tutum user and apikey to None"""
    tutum.user = None
    tutum.apikey = None


def load_from_file(file="~/.tutum"):
    """Attempts to read tutum's credentials from a config file and return a tuple of (user, apikey)

    :param file: The filename where Tutum auth config is stored
    :type file: str
    :returns: tuple -- tuple of (user, apikey) if config found and valid, (None, None) otherwise
    """
    try:
        cfgfile = os.path.expanduser(file)
        cp = configparser.ConfigParser()
        cp.read(cfgfile)
        return cp.get("auth", "user"), cp.get("auth", "apikey")
    except configparser.Error:
        return None, None


def get_auth_header():
    if tutum.user and tutum.apikey:
        return {'Authorization': 'ApiKey %s:%s' % (tutum.user, tutum.apikey)}
    else:
        return {}