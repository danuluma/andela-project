import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db1


class CategoryModel(Db1):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_categories(self):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM categories""")
    rows = cur.fetchall()
    orders = []
    for row in rows:
      print(row)
      item = {'id': row[0], 'name': row[1], 'description': row[2]}
      orders.append(item)
    print(orders)
    return orders

  def get_single_category(self, category_id):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM orders""")
    rows = cur.fetchall()
    order = []
    for row in rows:
      print(row)
      if row[0] == category_id :
          item = {'id': row[0], 'name': row[1], 'description': row[2]}
          order.append(item)
    print(order)
    return order

  def add_new_category(self, category_details):
    print(category_details)
    insertsql = """
    INSERT INTO categories (name, description)
    VALUES (%s,%s);
    """
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(insertsql, category_details)
    conn.commit()
    print("2 insert success")
    return {"Suceesss":"SSSS"}

  def update_category_details(self, category_id, categorydetails):

    updatesql = """UPDATE categories SET name = %s, description = %s WHERE id = {}""".format(category_id)
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(updatesql, categorydetails)
    conn.commit()
    selectsql = """SELECT * FROM categories WHERE id = {}""".format(category_id)
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)
    return record

  def delete_category(self, category_id):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    print("I'm about to delete")
    delsql = """DELETE FROM categories WHERE id = {}""".format(category_id)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},
