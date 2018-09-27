from flask import abort
from flask import request
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.dbconn import *

# createtables('DBASE')


createtables("DBASE")

menu = [
]

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('price', type=int,
  help='price can\'t be empty', required=True, location='json')
parser.add_argument('title', type=str,
  help='enter a name for the order',
  required=True, location='json')
parser.add_argument('category', type=str, location='json')
parser.add_argument('image_url', type=str, location='json')

class TestMe(Resource):
  """docstring for TestMe"""
  def get(self):
    return {"message":"It works"}

class Menu(Resource):
  """Endpoint for orders. ~/dann/api/v1/orders"""

  """Endpoint for GET requests. Retrieves the menu"""
  def get(self):
    mydb = 'DBASE'
    conn = connect_db(mydb)
    cur = conn.cursor()
    cur.execute('select * from menu')
    rows = cur.fetchall()
    menu = []
    for row in rows:
      print(row)
      item = {'id': row[0], 'title': row[1], 'category': row[2], 'description': row[3], 'image_url': row[4], 'price': row[5]}
      menu.append(item)
    print(menu)
    return {'menu': menu}, 200

  """Endpoint for POST requests. Creates a new order. Authentication is required"""
  # @jwt_required
  def post(self):
    mydb = 'DBASE'
    if not request.get_json(force=True):
      return {'Error':'Data is not application/json!!!'}, 404
    args = parser.parse_args()
    if args['title'] == "":
      return {'Error':'Order must have a valid title'}, 400
    menu = [
        args['title'],
        args['category'],
        args['description'],
        args['image_url'],
        args['price']
    ]

    insertsql = """
    INSERT INTO menu (title, category, description, image_url, price)
    VALUES (%s,%s,%s,%s,%s);
    """
    conn = connect_db(mydb)
    cur = conn.cursor()
    cur.execute(insertsql, menu)
    conn.commit()
    cur.execute('select * from menu')
    rows = cur.fetchall()
    menuitems = []
    for row in rows:
      item = {'id': row[0], 'title': row[1], 'category': row[2], 'description': row[3], 'image_url': row[4], 'price': row[5]}
      menuitems.append(item)
    print(menuitems)
    return {'menu': menuitems}, 201


# class MyOrder(Resource):
#   """Endpoint for specific orders. ~/dann/api/v1/order/<int:order_id>"""

#   """Endpoint for GET requests. Retrieves a specific order requested"""
#   def get(self, order_id):
#     order = [order for order in orders if order['id'] == order_id]
#     if len(order) == 0:
#       return {'Error':'Order does not exist'}, 404
#     return {'order': order[0]}, 200

#   """Endpoint for PUT requests. Edits a specific order with the new details passed in"""
#   @jwt_required
#   def put(self, order_id):
#     order = [order for order in orders if order['id'] == order_id]
#     args = parser.parse_args()
#     title = args['title']
#     description = args['description']
#     price = args['price']
#     if len(order) == 0:
#       return {'Error':'That order does not exist'}, 400

#     if title == "":
#       return {"Error": "Title can't be changed to null"}, 400

#     if description == "":
#       return {"Error": "Description can't be changed to null"}, 400

#     if price < 0:
#       return {"Error": "Price can't be less than zero"}, 400

#     order[0]['title'] = title
#     order[0]['description'] = description
#     order[0]['price'] = price
#     return {'order': order[0]}, 201
