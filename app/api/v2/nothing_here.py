import os, sys

from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
from instance.config import app_config
from app.api.v2.models.validate import Validate


load_dotenv('.env')

