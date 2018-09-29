import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.db import Db1


Db1("DBASE").create1()

# dont worry hapa ndio natest my stuff
