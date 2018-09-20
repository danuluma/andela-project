import os, psycopg2

def create_db():
  # conn = psycopg2.connect()
  try:
    conn = psycopg2.connect("dbname='dan' user='dan' host='localhost' password=''")
    print ("yeeah")
  except:
    print ("I am unable to connect to the database")


create_db()