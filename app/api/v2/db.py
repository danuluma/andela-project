import psycopg2
import psycopg2.extras
import os, sys
from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

load_dotenv('.env')



class Db1(object):
  """docstring for Db"""
  def __init__(self, mydb):
    self.dbase = os.getenv(mydb)

  def connect1(self):
    try:
        conn2 = psycopg2.connect(self.dbase)
        print("what")
    except:
        print("Ayam suffering, can't connect to the database2")

    return conn2

  def create1(self):
    try:
        conn2 = self.connect1()
        cur = conn2.cursor()
        file = open("app/api/v2/tcreate.sql", "r")
        sql = file.read()
        # print(sql)
        cur.execute(sql)
        conn2.commit()
        conn2.close()
        # print("created2")
        file.close()
    except:
        print("failed creating2")

  def drop1(self):
    try:
        conn2 = self.connect1()
        cur = conn2.cursor()
        file = open("app/api/v2/tdrop.sql", "r")
        sql = file.read()
        # print(sql)
        cur.execute(sql)
        conn2.commit()
        print("dropped2")
    except:
        print("failed dropping2")
    finally:
        file.close()

