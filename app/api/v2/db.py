import psycopg2
import psycopg2.extras
import os, sys
from flask import Flask

from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
from instance.config import app_config

load_dotenv('.env')




class Db(object):
  """docstring for Db"""
  def __init__(self):
    self.dbase = app_config["development"].DB_URI

  def connect(self):
    try:
        conn = psycopg2.connect(self.dbase)
        print(" connection OK")
        print(app_config["development"].DB_URI)
        print("up")

    except:
        print("can't connect to the database")
        print(app_config["development"].DB_URI)
        print("up")
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


  def create(self):
    file = open("app/api/v2/tcreate.sql", "r")
    return self.run_query(file)

  def drop(self):
    file = open("app/api/v2/tdrop.sql", "r")
    return self.run_query(file)

  def get_query(self, get_query):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(get_query)
    return cur.fetchall()

  def post_query(self, post_query, data):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(post_query, data)
    conn.commit()
    conn.close()

  def put_query(self, put_query, data, get_query):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(put_query, data)
    conn.commit()
    cur.execute(get_query)
    return cur.fetchone()

  def delete_query(self, delete_query):
    conn = self.connect()
    cur = conn.cursor()
    cur.execute(delete_query)
    conn.commit()
    conn.close()

  def get_all(self, name):
    items = []
    for row in self.get_query("""SELECT * FROM {}""".format(name)):
      item = {row}
      items.append(item)
    return items
