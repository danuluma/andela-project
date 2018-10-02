import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db1


class OrderModel(Db1):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_orders(self):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM orders""")
    rows = cur.fetchall()
    orders = []
    for row in rows:
      print(row)
      item = {'id': row[0], 'price': row[1], 'description': row[2], 'ordered_by': row[3], 'order_date': row[4], 'status': row[5]}
      orders.append(item)
    print(orders)
    return orders

  def get_single_order(self, order_id):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM orders""")
    rows = cur.fetchall()
    order = []
    for row in rows:
      print(row)
      if row[0] == order_id :
          item = {'id': row[0], 'price': row[1], 'description': row[2], 'ordered_by': row[3], 'order_date': row[4], 'status': row[5]}
          order.append(item)
    print(order)
    return order

  def get_user_order(self, ordered_by):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM orders""")
    rows = cur.fetchall()
    orders = []
    for row in rows:
      print(row)
      if row[3] == ordered_by :
          item = {'id': row[0], 'price': row[1], 'description': row[2], 'ordered_by': row[3], 'order_date': row[4], 'status': row[5]}
          orders.append(item)
    print(orders)
    return orders

  def add_new_order(self, order_details):
    print(order_details)
    insertsql = """
    INSERT INTO orders (price, description, ordered_by, status)
    VALUES (%s,%s,%s,%s);
    """
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(insertsql, order_details)
    conn.commit()
    print("2 insert success")
    return {"Suceesss":"SSSS"}

  def update_order_details(self, order_id, orderdetails):

    updatesql = """UPDATE orders SET price = %s, description = %s, ordered_by = %s, order_date = %s, status = %s WHERE id = {}""".format(order_id)
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    cur.execute(updatesql, orderdetails)
    conn.commit()
    selectsql = """SELECT * FROM orders WHERE id = {}""".format(order_id)
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)
    return record

  def delete_order(self, order_id):
    conn = Db1("DBASE").connect1()
    cur = conn.cursor()
    print("I'm about to delete")
    delsql = """DELETE FROM orders WHERE id = {0}""".format(order_id)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},
