from flask import abort
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.modelorder import OrderModel
from app.api.v2.models.menumodel import MenuModel


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('item_id', type=str, required=True, location='json')


class UserOrder(Resource):
  """Endpoints for a single user to view and place orders. ~/dann/api/v2/user/orders"""

  """Endpoint for GET requests. Retrieves the gets all orders for a user"""
  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    ordered_by = current_user[1]
    items = OrderModel.get_user_order(self, ordered_by)
    hist = []
    for item in items:
      m_item = {
      "order_id": item[0],
      "order_price": item[1],
      "details": item[2],
      "ordered_by": item[3],
      "order_status": item[5]
      }
      hist.append(m_item)
    return hist, 200

  """Endpoint for POST requests. Retrieves the creates an order for a user"""
  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    ordered_by = current_user[1]
    status = 0
    args = parser.parse_args()
    args['item_id']
    if MenuModel.get_menu_item(self, args['item_id']):
      item = MenuModel.get_menu_item(self, args['item_id'])
      args = parser.parse_args()
      print(item)

      order_details = [
          50,
          item,
          ordered_by,
          status
      ]
      OrderModel.add_new_order(self, order_details)
      return {"Success":"Order placed"}, 200
    else:
      return {"Error":"Item does not exist in menu"}, 404
