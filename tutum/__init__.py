import os, logging

user        = os.environ.get('TUTUM_USER')
apikey      = os.environ.get('TUTUM_APIKEY')

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)