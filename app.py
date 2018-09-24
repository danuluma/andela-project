from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)

orders = [
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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "Hi person ;-)"


@app.route('/dann/api/v1/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders})


@app.route('/dann/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = [order for order in orders if order['id'] == order_id ]
    if len(order) == 0:
        abort(404)
    return jsonify({'order': order[0]})


@app.route('/dann/api/v1/orders', methods=['POST'])
def create_order():
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


@app.route('/dann/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
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


if __name__ == '__main__':
    app.run(debug=True)
