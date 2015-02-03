import logging
import os

from future.standard_library import install_aliases
install_aliases()

from tutum.api import auth
from tutum.api.service import Service
from tutum.api.container import Container
from tutum.api.image import Image
from tutum.api.node import Node
from tutum.api.action import Action
from tutum.api.nodecluster import NodeCluster
from tutum.api.nodetype import NodeType
from tutum.api.nodeprovider import Provider
from tutum.api.noderegion import Region
from tutum.api.tag import Tag
from tutum.api.volume import Volume
from tutum.api.volumegroup import VolumeGroup
from tutum.api.webhookhandler import WebhookHandler
from tutum.api.exceptions import TutumApiError, TutumAuthError


__version__ = '0.11.2'

# : The username used to authenticate with the API
user = auth.load_from_file()[0] or os.environ.get('TUTUM_USER', None)

#: The ApiKey used to authenticate with the API
apikey = auth.load_from_file()[1] or os.environ.get('TUTUM_APIKEY', None)

#: The API endpoint to use
base_url = os.environ.get('TUTUM_BASE_URL', "https://dashboard.tutum.co/api/v1/")
tutum_auth = os.environ.get('TUTUM_AUTH', '')

logger = logging.getLogger("python-tutum")
