from dotenv import load_dotenv

import os

load_dotenv('.env')


class Config():
    DEBUG = False
    TESTING = False
    DB_URI = os.getenv("DBASE")

class ProductionConfig(Config):
    DB_URI = os.getenv("PBASE")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DB_URI = os.getenv("DBASE")



app_config = {
  "testing": TestingConfig,
  "development": DevelopmentConfig,
  "production": ProductionConfig
}