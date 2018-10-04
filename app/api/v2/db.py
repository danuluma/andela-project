import psycopg2
import psycopg2.extras
import os, sys
from flask import Flask

from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
from instance.config import app_config
from app.api.v2.create_tables import create_tables
from app.api.v2.drop_tables import drop_tables


load_dotenv('.env')


class Db(object):
  """docstring for Db"""
  def __init__(self):
    self.dbase = app_config["development"].DB_URI

  def connect(self):
    try:
        conn = psycopg2.connect(os.getenv("DBASE"))
    except:
        print("can't connect to the database")
    return conn


  def run_query(self, file):
    try:
        conn = self.connect()
        cur = conn.cursor()
        sql = file.read()
        cur.execute(sql)
        conn.commit()
        print("query ran successfully")
        file.close()
        conn.close()
    except:
        print("failed....")

  def creates(self):
    for query in create_tables:
      try:
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        cur.close
        # print("created successfully")
      except:
        print("Error occurred creation failed")
        print(query)

  def drops(self):
    for query in drop_tables:
      try:
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        cur.close
        # print("table dropped successfully")
      except:
        print("Error occurred dropping failed")


  def create(self):
    file = open("app/api/v2/tcreate.sql", "r")
    return self.run_query(file)

  def drop(self):
    file = open("app/api/v2/tdrop.sql", "r")
    return self.run_query(file)

  def get_query(self, table):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM {}""".format(table))
    return [row for row in cur.fetchall()]

  def post_query(self, post_query, data):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(post_query, data)
    conn.commit()
    conn.close()

  def put_query(self, put_query, data):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(put_query, data)
    conn.commit()

  def delete_query(self, delete_query):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(delete_query)
    conn.commit()
    conn.close()

