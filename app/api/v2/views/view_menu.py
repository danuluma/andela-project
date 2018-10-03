from flask import abort
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from run import *
import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.menumodel import MenuModel
from app.api.v2.models.validate import Validate


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
    return items, 200

  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      args = parser.parse_args()
      if not Validate().validate_name(args['title']):
        return {"Error":"Title should have at least 3 characters!"}
      if not Validate().validate_name(args['category']):
        return {"Error":"Category should have at least 3 characters!"}

      menu1 = [
          args['title'],
          args['category'],
          args['description'],
          args['image_url'],
          args['price']
      ]

      MenuModel.post_menu_item(self, menu1)
      return {"Mess":"Menu created sucessfully"}, 200
    else:
      return {"Error":"Only admins are allowed to create menu on other's behalf"}, 401

class MenuItem(Resource):
  """docstring for ClassName"""
  @jwt_required
  def get(self, item_id):
    print("Check below")
    current_user = get_jwt_identity()
    print(current_user)
    if current_user[2] == "admin":
      items = MenuModel.get_menu_item(self, item_id)
      print(items)
      # return {"Menu":items}
      return items, 200
    else:
      return {"Error":"Only admins are allowed to view this"}, 403

  @jwt_required
  def put(self, item_id):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      item = item_id
      args = parser.parse_args()
      if not Validate().validate_name(args['title']):
        return {"Error":"Title should have at least 3 characters!"}
      if not Validate().validate_name(args['category']):
        return {"Error":"Category should have at least 3 characters!"}

      menu1 = [
          args['title'],
          args['category'],
          args['description'],
          args['image_url'],
          args['price']
      ]

      MenuModel.update_menu_item(self, menu1, item)
      return {"Success":"Menu has been updated"}, 200
    else:
      return {"Error":"Only admins are allowed to edit this"}, 403

  @jwt_required
  def delete(self, item_id):
    current_user = get_jwt_identity()
    if current_user[2] == "admin":
      item = item_id
      MenuModel.delete_menu_item(self, item)
      return {"Success":"Menu has been deleted"}, 200
    else:
      return {"Error":"Only admins are allowed to delete this"}, 403