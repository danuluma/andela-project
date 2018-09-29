import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.db import Db1


class MenuModel(Db1):
  """docstring for Menu"""
  def __init__(self):
    pass
  # def __init__(self, title, category, description, image_url, price, item_id):
  #   super(MenuModel, self).__init__()
  #   self.title = title
  #   self.category = category
  #   self.description = description
  #   self.image_url = image_url
  #   self.price = price
  #   self.item_id = item_id

  def get_all_menu(self):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute('select * from menu')
    rows = cur.fetchall()
    menu = []
    for row in rows:
      print(row)
      item = {'id': row[0], 'title': row[1], 'category': row[2], 'description': row[3], 'image_url': row[4], 'price': row[5]}
      menu.append(item)
    print(menu)
    return menu

  def get_menu_item(self, item_id):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute('select * from menu')
    rows = cur.fetchall()
    menu_item = []
    for row in rows:
      print(row)
      if row[0] == item_id:
          item = {'id': row[0], 'title': row[1], 'category': row[2], 'description': row[3], 'image_url': row[4], 'price': row[5]}
          menu_item.append(item)
    print(menu_item)
    return menu_item

  def post_menu_item(self, menu1):
    print(menu1)
    insertsql = """
    INSERT INTO menu (title, category, description, image_url, price)
    VALUES (%s,%s,%s,%s,%s);
    """
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(insertsql, menu1)
    conn.commit()
    print("2 insert sucsess")
    return {"Suceesss":"SSSS"}

  def update_menu_item(self, menu, item_id):

    updatesql = """UPDATE menu SET title = %s, category = %s, description = %s, image_url = %s, price = %s WHERE id = {0}""".format(item_id)
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(updatesql, menu)
    conn.commit()
    selectsql= """SELECT * FROM menu WHERE id = {0}""".format(item_id)
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)
    return record

  def delete_menu_item(self, item_id):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    print("I'm about to delete")
    delsql= """DELETE FROM menu WHERE id = {0}""".format(item_id)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},
