from flask import abort
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.modelorder import OrderModel
from app.api.v2.models.validate import Validate


parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('status', type=str, default=0, location='json')


class OrdersView(Resource):
  """Endpoints for menu. ~/dann/api/v2/menu"""

  """Endpoint for GET requests. Retrieves the menu"""
  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      items = OrderModel.get_all_orders(self)
      hist = []
      for item in items:
        m_item = {
        "order_id": item[0],
        "order_price": item[1],
        "orderer": item[2],
        "date_ordered": item[3],
        "order_status": item[4]
        }
        hist.append(m_item)
      return hist, 200
    else:
      return {"Error":"Only admins are allowed to view all orders"}, 401


class OrderItem(Resource):
  """docstring for ClassName"""
  @jwt_required
  def get(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      item = OrderModel.get_single_order(self, orderId)
      print(item)
      return item, 200
    else:
      return {"Error":"Only admins are allowed to view a specific item"}, 401

  @jwt_required
  def put(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      args = parser.parse_args()

      args['status']

      OrderModel.update_order_status(self, orderId, args['status'])
      return {"Suceess":"Order has been updated"}, 200
    else:
      return {"Error":"Only admins are allowed to update the status of an order"}, 401

  @jwt_required
  def delete(self, order_id):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      OrderModel.delete_order(self, order_id)
      return {"Success":"Order has been deleted"}, 200
    else:
      return {"Error":"Only admins are allowed to delete an order"}, 401
