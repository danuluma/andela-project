from flask import abort
from flask import request
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.menumodel import MenuModel

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('price', type=int,
  help='price can\'t be empty', required=True, location='json')
parser.add_argument('title', type=str,
  help='enter a name for the menu item',
  required=True, location='json')
parser.add_argument('category', type=str, location='json')
parser.add_argument('image_url', type=str, location='json')


class MenuView(Resource):
  """Endpoints for menu. ~/dann/api/v2/menu"""

  """Endpoint for GET requests. Retrieves the menu"""
  def get(self):
    items = MenuModel.get_all_menu(self)
    print(items)
    # return {"Menu":items}
    return items

  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      args = parser.parse_args()

      menu1 = [
          args['title'],
          args['category'],
          args['description'],
          args['image_url'],
          args['price']
      ]

      MenuModel.post_menu_item(self, menu1)
      return {"Suceess":"Menu imeingia"}, 200
    else:
      return {"Error":"Only admins are allowed to create menu"}, 403

class MenuItem(Resource):
  """docstring for ClassName"""
  def get(self, item_id):
    items = MenuModel.get_menu_item(self, item_id)
    print(items)
    # return {"Menu":items}
    return items

  def put(self, item_id):
    item = item_id
    args = parser.parse_args()

    menu1 = [
        args['title'],
        args['category'],
        args['description'],
        args['image_url'],
        args['price']
    ]

    MenuModel.update_menu_item(self, menu1, item)
    return {"Suceess":"Menu has been updated"}

  def delete(self, item_id):
    item = item_id
    MenuModel.delete_menu_item(self, item)
    return {"Suceess":"Menu has been dleted"}
