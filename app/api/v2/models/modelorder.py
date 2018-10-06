import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class OrderModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass


  def format_order(self, items):
    order = []
    for item in items:
      m_item = {
      "order_id": item[0],
      "order_price": item[1],
      "details": item[2],
      "ordered_by": item[3],
      "order_status": item[5]
      }
      order.append(m_item)
    return order


  def get_all_orders(self):
    orders = Db().get_query('orders')
    return OrderModel().format_order(orders)

  def get_single_order(self, order_id):
    order = [row for row in Db().get_query('orders') if row[0]==order_id]
    return OrderModel().format_order(order)

  def get_user_order(self, ordered_by):
    rows = [row for row in Db().get_query('orders')]
    return OrderModel().format_order(rows)

  def add_new_order(self, order_details):
    Db().post_query("""
    INSERT INTO orders (price, description, ordered_by, status)
    VALUES (%s,%s,%s,%s);
    """, order_details)

  def update_order_details(self, order_id, orderdetails):

    updatesql = """UPDATE orders SET price = %s, description = %s, ordered_by = %s, order_date = %s, status = %s WHERE id = {}""".format(order_id)
    return Db().put_query(updatesql, orderdetails)

  def update_order_status(self, order_id, status):

    updatesql = """UPDATE orders SET status = %s WHERE id = {}""".format(order_id)
    return Db().put_query(updatesql, status)

  def delete_order(self, order_id):
    Db().delete_query("""DELETE FROM orders WHERE id = {0}""".format(order_id))
