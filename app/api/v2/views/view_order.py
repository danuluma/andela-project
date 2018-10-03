from flask import abort
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.modelorder import OrderModel

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('price', type=int,
                    help='price can\'t be empty', required=True, location='json')
parser.add_argument('ordered_by', type=str,
                    help='enter a name for the orderer',
                    required=True, location='json')
parser.add_argument('order_date', type=str, location='json')
parser.add_argument('status', type=str, default=0, location='json')


class OrdersView(Resource):
  """Endpoints for menu. ~/dann/api/v2/menu"""

  """Endpoint for GET requests. Retrieves the menu"""
  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      items = OrderModel.get_all_orders(self)
      return items, 200
    else:
      return {"Error":"Only admins are allowed to view all orders"}, 403


  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    if current_user[0] == "dan":
      args = parser.parse_args()

      order_details = [
          args['price'],
          args['description'],
          args['ordered_by'],
          args['status']
      ]

      OrderModel.add_new_order(self, order_details)
      return {"Suceess":"Order placed"}, 200
    else:
      return {"Error":"Only admins are allowed to view this"}, 403


class OrderItem(Resource):
  """docstring for ClassName"""
  @jwt_required
  def get(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      item = OrderModel.get_single_order(self, orderId)
      print(item)
      return item, 200
    else:
      return {"Error":"Only admins are allowed to view this"}, 403

  @jwt_required
  def put(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      args = parser.parse_args()

      order_details = [
          args['price'],
          args['description'],
          args['ordered_by'],
          args['status']
      ]

      OrderModel.update_order_details(self, orderId, order_details)
      return {"Suceess":"Order has been updated"}, 200
    else:
      return {"Error":"Only admins are allowed to view this"}, 403

  @jwt_required
  def delete(self, order_id):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      OrderModel.delete_order(self, order_id)
      return {"Suceess":"Order has been deleted"}, 200
    else:
      return {"Error":"Only admins are allowed to view this"}, 403
