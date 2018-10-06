import os, sys

from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
from instance.config import app_config

load_dotenv('.env')


print(app_config[os.getenv('APP_SETTINGS')].DB_URI)

