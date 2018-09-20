
from flask import abort
from flask import request
from flask_restful import Resource, reqparse


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

  def get(self):
    return {"message": "Hello, there ;-)"}, 200


class Orders(Resource):
  """docstring for Orders"""

  def get(self):
    return {'orders': orders}, 200

  def post(self):
    if not request.get_json(force=True):
      abort(404)
    args = parser.parse_args()
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
      abort(404)
    return {'order': order[0]}, 200

  def put(self, order_id):
    order = [order for order in orders if order['id'] == order_id]
    if len(order) == 0:
      abort(404)

    args = parser.parse_args()
    order[0]['title'] = args['title']
    order[0]['description'] = args['description']
    order[0]['price'] = args['price']
    return {'order': order[0]}, 201
