from dotenv import load_dotenv
import os
import sys

load_dotenv('.env')

class Testing(object):
  """
  Testing environment configuration
  """
  TESTING = True
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# class Development(object):
#   """
#   Development environment configuration
#   """
#   JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app_config = {
    'testing': Testing
 }