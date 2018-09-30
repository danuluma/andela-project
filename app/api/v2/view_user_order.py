from flask import abort
from flask import request
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.modelorder import OrderModel

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
  def get(self, ordered_by):
    ordered_by = "Dan"
    items = OrderModel.get_single_order(self, ordered_by)
    print(items)
    return items


  def post(self):
    ordered_by = "Dan"
    status = 0

    args = parser.parse_args()

    order_details = [
        args['price'],
        args['description'],
        ordered_by,
        status
    ]

    OrderModel.add_new_order(self, order_details)
    return {"Suceess":"Order placed"}
