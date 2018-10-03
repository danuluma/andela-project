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
parser.add_argument('item_id', type=str, location='json')


class UserOrder(Resource):
  """Endpoints for a single user to view and place orders. ~/dann/api/v2/user/orders"""

  """Endpoint for GET requests. Retrieves the gets all oredrs for a user"""
  # @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    ordered_by = "dan"
    items = OrderModel.get_user_order(self, ordered_by)
    return {"My orders": items}, 200

  # @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    ordered_by = "dan"
    status = 0
    args = parser.parse_args()
    item = MenuModel.get_menu_item(self, 1)
    print(item)

    order_details = [
        50,
        "haha",
        ordered_by,
        status
    ]
    OrderModel.add_new_order(self, order_details)
    return {"Success":"Order placed"}, 200
