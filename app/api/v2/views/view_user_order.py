from flask import abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
import os, sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')
# Local imports
from app.api.v2.models.modelorder import OrderModel
from app.api.v2.models.menumodel import MenuModel


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('item_id', type=int, required=True, location='json')


class UserOrder(Resource):
  """Endpoints for a single user to view and place orders. ~/dann/api/v2/user/orders"""

  """Endpoint for GET requests. Retrieves the gets all orders for a user"""
  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    ordered_by = current_user[1]
    hist = OrderModel.get_user_order(self, ordered_by)

    if len(hist)==0:
      return {"Message":"There's no history to show"},404
    return hist, 200

  """Endpoint for POST requests. It creates an order for a user"""
  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    ordered_by = current_user[0]
    status = 0
    args = parser.parse_args()
    args['item_id']
    item = MenuModel.get_menu_item(self, args['item_id'])
    if len(item) != 0:
      args = parser.parse_args()

      order_details = [
          50,
          item,
          ordered_by,
          status
      ]
      OrderModel.add_new_order(self, order_details)
      return {"Success":"Order placed"}, 201
    else:
      return {"Error":"Item does not exist in menu"}, 404

class Home1(Resource):
  """Just a test endpoint ~/"""
  def get(self):
    return "God's not dead, and so is Dann's api. Hello, there ;-)", 200

