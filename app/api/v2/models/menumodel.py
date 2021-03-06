import os, sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class MenuModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass


  def get_all_menu(self):
    return Db().get_query('menu')

  def get_menu_item(self, item_id):
    return [row for row in Db().get_query('menu') if row[0]==item_id]

  def post_menu_item(self, menu1):
    Db().post_query("""
    INSERT INTO menu (title, category, description, image_url, price)VALUES (%s,%s,%s,%s,%s);
    """, menu1)

  def update_menu_item(self, menu, item_id):

    updatesql = """UPDATE menu SET title = %s, category = %s, description = %s, image_url = %s, price = %s WHERE id = {}""".format(item_id)
    return Db().put_query(updatesql, menu)

  def delete_menu_item(self, item_id):
    Db().delete_query("""DELETE FROM menu WHERE id = {}""".format(item_id))

