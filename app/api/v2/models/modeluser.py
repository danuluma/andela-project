import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db1


class UserModel(Db1):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_users(self):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users""")
    rows = cur.fetchall()
    users = []
    for row in rows:
      print(row)
      item = {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'email': row[4], 'password': row[5], 'phone': row[6], 'role': row[7]}
      users.append(item)
    print(users)
    return users

  def get_single_user(self, username, email):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    # cur.execute("""SELECT * FROM users WHERE username = {0} or email = {1}""".format(username, email))
    cur.execute("""SELECT * FROM users""")
    rows = cur.fetchall()
    user = []
    for row in rows:
      print(row)
      if row[3] == username or row[4] == email:
          item = {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'email': row[4], 'password': row[5], 'phone': row[6], 'role': row[7]}
          user.append(item)
    print(user)
    return user[0]

  def add_new_user(self, user):
    print(user)
    insertsql = """
    INSERT INTO users (first_name, last_name, username, email, password, phone, role)
    VALUES (%s,%s,%s,%s,%s,%s,%s);
    """
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(insertsql, user)
    conn.commit()
    print("2 insert success")
    return {"Suceesss":"SSSS"}

  def update_user_details(self, username, userdetails):

    updatesql = """UPDATE users SET first_name = %s, last_name = %s, username = %s, email = %s, password = %s, phone = %s, phone = %s WHERE username = {}""".format(username)
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(updatesql, userdetails)
    conn.commit()
    selectsql = """SELECT * FROM users WHERE username = {}""".format(username)
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)
    return record

  def delete_user(self, username):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    print("I'm about to delete")
    delsql = """DELETE FROM users WHERE username = {0}""".format(username)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},
