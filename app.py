from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response

app = Flask(__name__)

orders = [
    {
    'id': 1,
    'title': 'pancake',
    'description':'Lorem ipsum',
    'price': 50
    },
    {
    'id': 2,
    'title': 'pizza',
    'description':'Lorem ipsum',
    'price': 500
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "Hi person ;-)"

@app.route('/dann/api/v1.0/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders})

@app.route('/dann/api/v1.0/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order =[order for order in orders if order['id'] == order_id ]
    if len(order)==0:
        abort(404)
    return jsonify({'order': order[0]})

if __name__ == '__main__':
    app.run(debug=True)
