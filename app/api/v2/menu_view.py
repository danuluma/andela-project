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


class MenuItem(Resource):
  """docstring for MenuItem"""
  def put(self, item_id):
    mydb = 'DBASE'
    conn = connect_db(mydb)
    cur = conn.cursor()
    print("Table Before updating record ")
    selectsql= """SELECT * FROM menu WHERE id = {0}""".format(item_id)

    cur.execute(selectsql)
    item = cur.fetchone()
    print(item)

    args = parser.parse_args()

    menu = [
        args['title'],
        args['category'],
        args['description'],
        args['image_url'],
        args['price']
    ]

    # Update record now
    updatesql = """UPDATE menu SET title = %s, category = %s, description = %s, image_url = %s, price = %s WHERE id = {0}""".format(item_id)
    cur.execute(updatesql, menu)
    conn.commit()
    cur.execute(selectsql)
    record = cur.fetchone()
    print(record)

    return {'menu': record}, 201


  def delete(self, item_id):
    mydb = 'DBASE'
    conn = connect_db(mydb)
    cur = conn.cursor()
    print("Table Before updating record ")
    delsql= """DELETE FROM menu WHERE id = {0}""".format(item_id)
    cur.execute(delsql)
    conn.commit()

    return {"details":"done"},

