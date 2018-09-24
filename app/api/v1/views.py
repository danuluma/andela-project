
from flask import abort
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from run import *


orders = [
]

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('title', type=str,
  help='enter a name for the order',
  required=True, location='json')
parser.add_argument('description', type=str, location='json')
parser.add_argument('price', type=int,
  help='price can\'t be empty', required=True, location='json')


class Home(Resource):
  """docstring for Home"""
  # @jwt_required
  def get(self):
    return {"message": "Hello, there ;-)"}, 200


class Orders(Resource):
  """docstring for Orders"""

  def get(self):
    return {'orders': orders}, 200

  # @jwt_required
  def post(self):
    if not request.get_json(force=True):
      return {'Error':'Data is not application/json!!!'}, 404
    args = parser.parse_args()
    order = [order for order in orders if order['title'] == args['title'] ]
    if len(order) != 0:
      return {'Error':'Order already exists'}, 400
    order = {
        'id': len(orders) + 1,
        'title': args['title'],
        'description': args['description'],
        'price': args['price']
    }
    orders.append(order)
    return {'order': order}, 201


class MyOrder(Resource):
  """docstring for MyOrder"""

  def get(self, order_id):
    order = [order for order in orders if order['id'] == order_id]
    if len(order) == 0:
      return {'Error':'Order does not exist'}, 400
    return {'order': order[0]}, 200

  # @jwt_required
  def put(self, order_id):
    order = [order for order in orders if order['id'] == order_id]
    if len(order) == 0:
      return {'Error':'That order does not exist'}, 400

    args = parser.parse_args()
    order[0]['title'] = args['title']
    order[0]['description'] = args['description']
    order[0]['price'] = args['price']
    return {'order': order[0]}, 201
