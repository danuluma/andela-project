import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class CategoryModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def run_db_query(self, sql):
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(sql)

  def get_all_categories(self):
    orders = []
    for row in Db().get_query("""SELECT * FROM categories"""):
      print(row)
      item = {'id': row[0], 'name': row[1], 'description': row[2]}
      orders.append(item)
    print(orders)
    return orders

  def get_single_category(self, category_id):
    order = []
    for row in Db().get_query("""SELECT * FROM categories"""):
      print(row)
      if row[0] == category_id :
          item = {'id': row[0], 'name': row[1], 'description': row[2]}
          order.append(item)
    print(order)
    return order

  def add_new_category(self, category_details):
    Db().post_query("""
    INSERT INTO categories (name, description)
    VALUES (%s,%s);
    """, category_details)

  def update_category_details(self, category_id, categorydetails):

    updatesql = """UPDATE categories SET name = %s, description = %s WHERE id = {}""".format(category_id)
    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(updatesql, categorydetails)
    conn.commit()
    selectsql = """SELECT * FROM categories WHERE id = {}""".format(category_id)
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)
    return record

  def delete_category(self, category_id):
    conn = Db().connect()
    cur = conn.cursor()
    print("I'm about to delete")
    delsql = """DELETE FROM categories WHERE id = {}""".format(category_id)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},
