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
parser.add_argument('price', type=int, location='json')
parser.add_argument('title', type=str, location='json')
parser.add_argument('category', type=str, location='json')
parser.add_argument('image_url', type=str, location='json')


class MenuView(Resource):
  """Endpoints for menu. ~/dann/api/v2/menu"""

  """Endpoint for GET requests. Retrieves the menu"""
  def get(self):
    items = MenuModel.get_all_menu(self)
    menu = []
    for item in items:
      menuitem = {

      "id": item[0],
      "food-name": item[1],
      "food-category": item[2],
      "description": item[3],
      "image": item[4],
      "price": item[5]
      }

      menu.append(menuitem)
    return menu, 200

  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      args = parser.parse_args()
      if not Validate().validate_name(args['title']):
        return {"Error":"Title should have at least 3 characters!"}, 400
      if not Validate().validate_name(args['category']):
        return {"Error":"Category should have at least 3 characters!"}, 400

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
      return {"Error":"Only admins are allowed to create a menu item"}, 401

class MenuItem(Resource):
  """docstring for ClassName"""
  @jwt_required
  def get(self, item_id):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      item = MenuModel.get_menu_item(self, item_id)
      return {

      "id": item[0][0],
      "food-name": item[0][1],
      "food-category": item[0][2],
      "description": item[0][3],
      "image": item[0][4],
      "price": item[0][5]
      }, 200
    else:
      return {"Error":"Only admins are allowed to view this"}, 401

  @jwt_required
  def put(self, item_id):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      item = item_id
      args = parser.parse_args()
      if not Validate().validate_name(args['title']):
        return {"Error":"Title should have at least 3 characters!"}, 400
      if not Validate().validate_name(args['category']):
        return {"Error":"Category should have at least 3 characters!"}, 400

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
      return {"Error":"Only admins are allowed to edit this"}, 401

  @jwt_required
  def delete(self, item_id):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      item = item_id
      MenuModel.delete_menu_item(self, item)
      return {"Success":"Menu has been deleted"}, 200
    else:
      return {"Error":"Only admins are allowed to delete this"}, 401