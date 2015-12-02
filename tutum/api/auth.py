from __future__ import absolute_import
import base64
import json
import os
import tutum
from requests.auth import HTTPBasicAuth
from .http import send_request


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


# def load_from_file(file="~/.docker/config.json", site="https://index.docker.io/v1/"):
def load_from_file(file="~/.tutum", site="tutum.co"):
    """Attempts to read tutum's credentials from a config file

    :param file: The filename where the auth config is stored
    :type file: str
    :param site: load which website's auth
    :type site: str
    :returns: str -- the auth of the give website. empty string, when error occurs
    """
    try:
        with open(os.path.expanduser(file)) as f:
            data = f.read()
            cfg = json.loads(data)
        auth = cfg.get("auths", {}).get(site, {}).get("auth")
        return auth
    except Exception as e:
        return None


def get_auth_header():
    if tutum.tutum_auth:
        return {'Authorization': tutum.tutum_auth}
    if tutum.apikey_auth:
        return {'Authorization': 'Apikey %s' % tutum.apikey_auth}
    if tutum.basic_auth:
        return {'Authorization': 'Basic %s' % tutum.basic_auth}
    return {}
