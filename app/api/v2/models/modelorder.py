import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class OrderModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_orders(self):
    return Db().get_query('orders')

  def get_single_order(self, order_id):
    return [row for row in Db().get_query('orders') if row[0]==order_id]

  def get_user_order(self, ordered_by):
    orders = []
    for row in Db().get_query("""SELECT * FROM orders"""):
      print(row)
      if row[3] == ordered_by :
          item = {'id': row[0], 'price': row[1], 'description': row[2], 'ordered_by': row[3], 'order_date': row[4], 'status': row[5]}
          orders.append(item)
    print(orders)
    return orders

  def add_new_order(self, order_details):
    Db().post_query("""
    INSERT INTO orders (price, description, ordered_by, status)
    VALUES (%s,%s,%s,%s);
    """, order_details)

  def update_order_details(self, order_id, orderdetails):

    updatesql = """UPDATE orders SET price = %s, description = %s, ordered_by = %s, order_date = %s, status = %s WHERE id = {}""".format(order_id)
    selectsql = """SELECT * FROM orders WHERE id = {}""".format(order_id)
    return Db().put_query(updatesql, orderdetails, selectsql)

  def delete_order(self, order_id):
    Db().delete_query("""DELETE FROM orders WHERE id = {0}""".format(order_id))
