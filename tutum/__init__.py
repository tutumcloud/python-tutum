import logging
import os
from tutum.api import auth
from tutum.api.application import Application
from tutum.api.container import Container
from tutum.api.registry import Registry
from tutum.api.role import Role
from tutum.api.image import Image


user = auth.load_from_file()[0] or os.environ.get('TUTUM_USER', None)
apikey = auth.load_from_file()[1] or os.environ.get('TUTUM_APIKEY', None)
base_url = os.environ.get('TUTUM_BASE_URL', "https://app.tutum.co/api/v1/")
logger = logging.getLogger("python-tutum")