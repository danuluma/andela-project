from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_restful import Resource

orders = [
]


class Home(Resource):
  """docstring for Home"""

  def get(self):
    return {"message": "Hello, there ;-)"}


class Orders(Resource):
  """docstring for Orders"""

  def get(self):
    return jsonify({'orders': orders})

  def post(self):
    if not request.get_json(force=True):
      abort(404)
    order = {
        'id': len(orders) + 1,
        'title': request.get_json(force=True)['title'],
        'description': request.get_json(force=True)['description'],
        'price': request.get_json(force=True)['price']
    }
    orders.append(order)
    return make_response(jsonify({'order': order}), 201)


class MyOrder(Resource):
  """docstring for MyOrder"""

  def get(self, order_id):
    order = [order for order in orders if order['id'] == order_id]
    if len(order) == 0:
      abort(404)
    return make_response(jsonify({'order': order[0]}))

  def put(self, order_id):
    order = [order for order in orders if order['id'] == order_id]
    if len(order) == 0:
      abort(404)
    if not request.get_json(force=True):
      abort(404)
    order[0]['title'] = request.get_json(force=True)['title']
    order[0]['description'] = request.get_json(force=True)['description']
    order[0]['price'] = request.get_json(force=True)['price']
    return make_response(jsonify({'order': order[0]}), 201)
