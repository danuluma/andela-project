import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.dbconn import *

class Apiv2Test(unittest.TestCase):
  """ Tests for api v2 endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    createtables('DBASE')

  def tearDown(self):
    droptables('DBASE')

if __name__ == '__main__':
  unittest.main()
