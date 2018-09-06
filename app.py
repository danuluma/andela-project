from flask import Flask
from flask import jsonify

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

@app.route('/')
def index():
    return "Hi person ;-)"

@app.route('/dann/api/v1.0/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders})

if __name__ == '__main__':
    app.run(debug=True)
