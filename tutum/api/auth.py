from __future__ import absolute_import
import base64
import json
import os
import tutum
from requests.auth import HTTPBasicAuth
from .http import send_request
import configparser


def authenticate(username, password):
    """Authenticates a Tutum user using username and password. If successful, automatically sets ``tutum.user`` and ``tutum.apikey``

    :param username: The username of the user to authenticate
    :type username: str.
    :param password: The password of the user to authenticate
    :type password: str.
    :raises: TutumAuthError
    """
    verify_credential(username, password)
    tutum.basic_auth = base64.b64encode("%s:%s" % (username, password))


def verify_credential(username, password):
    """verify if username/password incorrect

    :param username: The username/email of the user to authenticate
    :type username: str
    :param password: The password of the user to authenticate
    :type password: str
    :raises: TutumAuthError
    :returns: str, str -- the Username, ApiKey to use for the given username/email
    """
    auth = HTTPBasicAuth(username, password)
    send_request("GET", "/auth", auth=auth)


def is_authenticated():
    """Returns whether the tutum user and apikey are set

    :returns: bool -- whether the tutum user and apikey are set
    """
    return tutum.tutum_auth or tutum.apikey_auth or tutum.basic_auth


def logout():
    """Sets the tutum user and apikey to None"""
    tutum.tutum_auth = None
    tutum.apikey_auth = None
    tutum.basic_auth = None


def load_from_file(f="~/.tutum"):
    """Attempts to read tutum's credentials from a config file

    :param f: The filename where the auth config is stored
    :type f: str
    :returns: str, str -- the basic auth and apikey auth
    """
    try:
        cp = configparser.SafeConfigParser({'user': None, 'apikey': None, 'basic_auth': None})
        cp.read(os.path.expanduser(f))
        basic_auth = cp.get("auth", "basic_auth")
        user = cp.get("auth", "user")
        apikey = cp.get("auth", "apikey")
        if user and apikey:
            apikey_auth = "%s:%s" % (user, apikey)
        else:
            apikey_auth = None
        return basic_auth, apikey_auth
    except Exception:
        return None, None


def get_auth_header():
    try:
        tutum.basic_auth = base64.b64encode("%s:%s" % (tutum.user, tutum.apikey))
    except:
        pass

    if tutum.tutum_auth:
        return {'Authorization': tutum.tutum_auth}
    if tutum.basic_auth:
        return {'Authorization': 'Basic %s' % tutum.basic_auth}
    return {}
