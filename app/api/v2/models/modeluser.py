import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class UserModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_users(self):
    return Db().get_query('users')

  def get_single_user(self, username, email):
    return [row for row in Db().get_query('users') if row[3] == username or row[4] == email]

  def add_new_user(self, user):
    Db().post_query("""
    INSERT INTO users (first_name, last_name, username, email, password, phone, role)
    VALUES (%s,%s,%s,%s,%s,%s,%s);
    """, user)

  def update_user_details(self, username, userdetails):

    updatesql = """UPDATE users SET first_name = %s, last_name = %s, username = %s, email = %s, password = %s, phone = %s, phone = %s WHERE username = {}""".format(username)
    return Db().put_query(updatesql, userdetails)

  def delete_user(self, username):
    Db().delete_query("""DELETE FROM users WHERE username = {0}""".format(username))
