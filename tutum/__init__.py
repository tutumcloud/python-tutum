import logging
import os

import requests
from future.standard_library import install_aliases

install_aliases()

from tutum.api import auth
from tutum.api.service import Service
from tutum.api.container import Container
from tutum.api.image import Image
from tutum.api.imagetag import ImageTag
from tutum.api.node import Node
from tutum.api.action import Action
from tutum.api.nodecluster import NodeCluster
from tutum.api.nodetype import NodeType
from tutum.api.nodeprovider import Provider
from tutum.api.noderegion import Region
from tutum.api.tag import Tag
from tutum.api.volume import Volume
from tutum.api.volumegroup import VolumeGroup
from tutum.api.trigger import Trigger
from tutum.api.stack import Stack
from tutum.api.exceptions import TutumApiError, TutumAuthError, ObjectNotFound, NonUniqueIdentifier
from tutum.api.utils import Utils
from tutum.api.events import TutumEvents
from tutum.api.nodeaz import AZ

__version__ = '0.20.1'

# : The username used to authenticate with the API
user = os.environ.get('TUTUM_USER', None) or auth.load_from_file()[0]

#: The ApiKey used to authenticate with the API
apikey = os.environ.get('TUTUM_APIKEY', None) or auth.load_from_file()[1]

#: The API endpoint to use
rest_host = os.environ.get('TUTUM_REST_HOST', 'https://dashboard.tutum.co')
stream_host = os.environ.get('TUTUM_STREAM_HOST', 'wss://stream.tutum.co')

base_url = os.environ.get('TUTUM_BASE_URL', "/".join([rest_host.rstrip("/"), "api/v1/"]))
stream_url = os.environ.get('TUTUM_STREAM_URL',  "/".join([stream_host.rstrip("/"), "v1/"]))

tutum_auth = os.environ.get('TUTUM_AUTH', '')

user_agent = None

logging.basicConfig()
logger = logging.getLogger("python-tutum")

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
