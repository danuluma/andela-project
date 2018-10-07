from flask import abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
import os, sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')
# Local imports here
from app.api.v2.models.modelorder import OrderModel
from app.api.v2.models.validate import Validate


parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('status', type=str, default=0, location='json')


class OrdersView(Resource):
  """Endpoints for orders. ~/dann/api/v2/orders"""

  """Endpoint for GET requests. Retrieves all orders"""
  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      return OrderModel.get_all_orders(self), 200
    else:
      return {"Error":"Only admins are allowed to view all orders"}, 401


class OrderItem(Resource):
  """docstring for OrderItem"""

  """Endpoint for GET requests. Retrieves a single order """

  @jwt_required
  def get(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      return OrderModel.get_single_order(self, orderId), 200
    else:
      return {"Error":"Only admins are allowed to view a specific item"}, 401

  """Endpoint for PUT requests. Updates status of an order"""
  @jwt_required
  def put(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      args = parser.parse_args()

      args['status']

      OrderModel.update_order_status(self, orderId, args['status'])
      return {"Suceess":"Order status has been updated"}, 200
    else:
      return {"Error":"Only admins are allowed to update the status of an order"}, 401

  """Endpoint for DELETE requests. Deletes an order"""
  @jwt_required
  def delete(self, orderId):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      OrderModel.delete_order(self, orderId)
      return {"Success":"Order has been deleted"}, 204
    else:
      return {"Error":"Only admins are allowed to delete an order"}, 401
