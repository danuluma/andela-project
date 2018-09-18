from flask_restful import Resource
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request


orders = [
 {
  'id': 1,
  'details': [
    {'title': 'pancake',
    'description': 'Lorem ipsum',
    'quantity': 3,
    'price': 50},
    {'title': 'pancake',
    'description': 'Lorem ipsum',
    'quantity': 1,
    'price': 50}]
 },
 {
  'id': 2,
  'details': [
    {'title': 'pizza',
    'description': 'Lorem ipsum',
    'quantity': 1,
    'price': 500},
    {'title': 'pizza',
    'description': 'Lorem ipsum',
    'quantity': 1,
    'price': 500}]
 }
]

foods = [
 {
  'id': 1,
  'title': 'pancake',
  'description': 'Lorem ipsum',
  'price': 50
 },
 {
  'id': 2,
  'title': 'pizza',
  'description': 'Lorem ipsum',
  'price': 500
 }
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
    if not request.json or'title' not in request.json:
        abort(404)
    order = {
        'id': orders[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'price': 0
    }
    orders.append(order)
    return jsonify({'order': order}), 201


class MyOrder(Resource):
  """docstring for MyOrder"""
  def get(self, order_id):
    order = [order for order in orders if order['id'] == order_id ]
    if len(order) == 0:
        abort(404)
    return jsonify({'order': order[0]})

  def put(self, order_id):
    order = [order for order in orders if order['id'] == order_id]
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    order[0]['title'] = request.json.get('title', order[0]['title'])
    order[0]['description'] = request.json.get('description', order[0]['description'])
    order[0]['price'] = request.json.get('price', order[0]['price'])
    return jsonify({'order': order[0]}), 201


class Foods(Resource):
  """docstring for Orders"""
  def get(self):
    return jsonify({'foods': foods})

  def post(self):
    if not request.json or'title' not in request.json:
        abort(404)
    food = {
        'id': foods[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'price': 0
    }
    foods.append(food)
    return jsonify({'food': food}), 201


class ThisFood(Resource):
  """docstring for MyOrder"""
  def get(self, food_id):
    food = [food for food in foods if food['id'] == food_id ]
    if len(food) == 0:
        abort(404)
    return jsonify({'food': food[0]})

  def put(self, food_id):
    food = [food for food in foods if food['id'] == food_id]
    if len(food) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    food[0]['title'] = request.json.get('title', food[0]['title'])
    food[0]['description'] = request.json.get('description', food[0]['description'])
    food[0]['price'] = request.json.get('price', food[0]['price'])
    return jsonify({'food': food[0]}), 201


