import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class MenuModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass


  def get_all_menu(self):
    menu = []
    for row in Db().get_query("""SELECT * FROM menu"""):
      item = {'id': row[0], 'title': row[1], 'category': row[2], 'description': row[3], 'image_url': row[4], 'price': row[5]}
      menu.append(item)
    return menu

  def get_menu_item(self, item_id):
    menu_item = []
    for row in Db().get_query("""SELECT * FROM menu"""):
      if row[0] == item_id:
          item = {'id': row[0], 'title': row[1], 'category': row[2], 'description': row[3], 'image_url': row[4], 'price': row[5]}
          menu_item.append(item)
    return menu_item

  def post_menu_item(self, menu1):
    Db().post_query("""
    INSERT INTO menu (title, category, description, image_url, price)VALUES (%s,%s,%s,%s,%s);
    """, menu1)

  def update_menu_item(self, menu, item_id):

    updatesql = """UPDATE menu SET title = %s, category = %s, description = %s, image_url = %s, price = %s WHERE id = {}""".format(item_id)
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(updatesql, menu)
    conn.commit()
    selectsql= """SELECT * FROM menu WHERE id = {}""".format(item_id)
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)
    return record

  def delete_menu_item(self, item_id):
    conn = Db().connect()
    cur = conn.cursor()
    print("I'm about to delete")
    delsql= """DELETE FROM menu WHERE id = {}""".format(item_id)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},
