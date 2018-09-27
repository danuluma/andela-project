import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.dbconn import *

droptables('DBASE')
