import os
import logging
from tutum.api.application import Application
from tutum.api.container import Container


user = os.environ.get('TUTUM_USER')
apikey = os.environ.get('TUTUM_APIKEY')
base_url = os.environ.get('TUTUM_BASE_URL', "https://app.tutum.co/api/v1/")

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)