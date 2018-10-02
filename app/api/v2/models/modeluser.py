import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class UserModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_users(self):
    users = []
    for row in Db().get_query("""SELECT * FROM users"""):
      item = {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'email': row[4], 'password': row[5], 'phone': row[6], 'role': row[7]}
      users.append(item)
    return users

  def get_single_user(self, username, email):
    user = []
    for row in Db().get_query("""SELECT * FROM users"""):
      if row[3] == username or row[4] == email:
          item = {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'email': row[4], 'password': row[5], 'phone': row[6], 'role': row[7]}
          user.append(item)
    return user[0]

  def add_new_user(self, user):
    Db().post_query("""
    INSERT INTO users (first_name, last_name, username, email, password, phone, role)
    VALUES (%s,%s,%s,%s,%s,%s,%s);
    """, user)

  def add_admin_user(self):
    Db().post_query("""
    INSERT INTO users (first_name, last_name, username, email, password, phone, role)
    VALUES ('admin','user','admin','secret@admin','admin','0701234567','admin');
    """, None)

  def update_user_details(self, username, userdetails):

    updatesql = """UPDATE users SET first_name = %s, last_name = %s, username = %s, email = %s, password = %s, phone = %s, phone = %s WHERE username = {}""".format(username)
    selectsql = """SELECT * FROM users WHERE username = {}""".format(username)
    return Db().put_query(updatesql, userdetails, selectsql)

  def delete_user(self, username):
    Db().delete_query("""DELETE FROM users WHERE username = {0}""".format(username))
