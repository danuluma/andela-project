import psycopg2
import psycopg2.extras
import os, sys
from flask import Flask

from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
# Local imports below
from app.config import app_config
from app.api.v2.create_tables import create_tables
from app.api.v2.drop_tables import drop_tables


load_dotenv('.env')


class Db(object):
  """docstring for Db"""
  def __init__(self):
    self.dbase = app_config[os.getenv('APP_SETTINGS')].DB_URI

  def connect(self):
    try:
        conn = psycopg2.connect(self.dbase)
    except:
        print("can't connect to the database")
    return conn


  def run_query(self, file):
    for query in file:
      try:
          conn = Db().connect()
          cur = conn.cursor()
          cur.execute(query)
          conn.commit()
          file.close()
          conn.close()
      except:
        pass
  def creates(self):
    Db().run_query(create_tables)

  def drops(self):
    Db().run_query(create_tables)

  def get_query(self, table):
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM {}""".format(table))
    return [row for row in cur.fetchall()]

  def post_query(self, post_query, data):
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(post_query, data)
    conn.commit()
    conn.close()

  def put_query(self, put_query, data):
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(put_query, data)
    conn.commit()

  def delete_query(self, delete_query):
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(delete_query)
    conn.commit()
    conn.close()

