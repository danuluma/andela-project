# import os, sys
# LOCALPATH = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, LOCALPATH + '/../../../')

# from app.api.v2.dbconn import *

# # createtables('DBASE')

# test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
#                         "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}

# # insertintotable('DBASE')

# def checkthis(mydb):
#   # insertdata = ('dan', 'blah', 'dan', 'dan', 'blah', 'dan')
#   relevant_keys = ('first_name', 'last_name', 'username', 'email', 'password', 'phone')
#   insertdata = [test_user2[key] for key in relevant_keys]
#   print(insertdata)
#   print("upppppppuuuuu")
#   insertsql = """
#   INSERT INTO users (first_name, last_name, username, email, password, phone)
#   VALUES (%s,%s,%s,%s,%s,%s);
#   """
#   conn = connect_db(mydb)
#   cur = conn.cursor()
#   cur.execute(insertsql, insertdata)
#   conn.commit()
#   cur.execute('select * from users')
#   rows = cur.fetchall()
#   for row in rows:
#     print(row)
#     user = {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'email': row[4], 'password': row[5], 'phone': row[6]}
#   print(user)


# createtables('DBASE')

# checkthis('DBASE')