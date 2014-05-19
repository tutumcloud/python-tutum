import logging
import os
from tutum.api import auth
from tutum.api.application import Application
from tutum.api.container import Container
from tutum.api.registry import Registry
from tutum.api.image import Image
from tutum.api.exceptions import TutumApiError, TutumAuthError

__version__ = '0.7.2'

#: The username used to authenticate with the API
user = auth.load_from_file()[0] or os.environ.get('TUTUM_USER', None)

#: The ApiKey used to authenticate with the API
apikey = auth.load_from_file()[1] or os.environ.get('TUTUM_APIKEY', None)

#: The API endpoint to use
base_url = os.environ.get('TUTUM_BASE_URL', "https://app.tutum.co/api/v1/")

logger = logging.getLogger("python-tutum")
