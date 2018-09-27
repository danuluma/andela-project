import psycopg2
import psycopg2.extras
import os, sys
from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

load_dotenv('.env')


def connect_db(mydb):
    dbase = os.getenv(mydb)
    try:
        conn = psycopg2.connect(dbase)
        print("yeeah")
    except:
        print("Ayam suffering, can't connect to the database")

    return conn


def createtables(mydb):
    try:
        conn = connect_db(mydb)
        cur = conn.cursor()
        file = open("app/api/v2/tcreate.sql", "r")
        sql = file.read()
        print(sql)
        cur.execute(sql)
        conn.commit()
        print("created")
        file.close()
    except:
        print("failed creating")

# def insertintotable(mydb):
#     insertdata = ('dan', 'blah', 'dan', 'dan', 'blah', 'dan')
#     name = 'users'
#     insertsql = """
#     INSERT INTO users (first_name, last_name, username, email, password, phone)
#     VALUES (%s,%s,%s,%s,%s,%s);
#     """
#     conn = connect_db(mydb)
#     cur = conn.cursor()
#     cur.execute(insertsql, insertdata)
#     conn.commit()
#     cur.execute('select * from users')
#     rows = cur.fetchall()
#     for row in rows:
#       print(row)
#     print("got it")


def droptables(mydb):
    try:
        conn = connect_db(mydb)
        cur = conn.cursor()
        file = open("app/api/v2/tdrop.sql", "r")
        sql = file.read()
        print(sql)
        cur.execute(sql)
        conn.commit()
        print("dropped")
    except:
        print("failed dropping")
    finally:
        file.close()
