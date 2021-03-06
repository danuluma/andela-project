from flask import abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
import os, sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')
# Local imports now
from app.api.v2.models.menumodel import MenuModel
from app.api.v2.models.validate import Validate


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('price', type=int, location='json')
parser.add_argument('title', type=str, location='json')
parser.add_argument('category', type=str, location='json')
parser.add_argument('image_url', type=str, location='json')

def create_menu(self):
  args = parser.parse_args()
  menu = [
        args['title'],
        args['category'],
        args['description'],
        args['image_url'],
        args['price']
    ]
  return menu


def check_valid(self):
  args = parser.parse_args()
  errors = []
  if not Validate().validate_name(args['title']):
    errors.append({"Error":"Title should have at least 3 characters!"})
  if not Validate().validate_name(args['category']):
    errors.append({"Error":"Category should have at least 3 characters!"})
  return errors


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
    if len(menu) == 0:
      return {"Message":"No menu item present"}, 404
    return menu, 200

  """Endpoint for POST requests. Creates a menu item"""
  @jwt_required
  def post(self):
    current_user = get_jwt_identity()
    role = current_user[2]
    if role == 1:
      args = parser.parse_args()
      if len(check_valid(self)) == 0:
        MenuModel.post_menu_item(self, create_menu(self))
        return {"Mess":"Menu item added successfully"}, 200
      return check_valid(self)
    else:
      return {"Error":"Only admins are allowed to create a menu item"}, 401

class MenuItem(Resource):
  """docstring for MenuItem"""

  """Endpoint for GET requests. Retrieves a single menu item"""
  def get(self, item_id):
      item = MenuModel.get_menu_item(self, item_id)
      return {

      "id": item[0][0],
      "food-name": item[0][1],
      "food-category": item[0][2],
      "description": item[0][3],
      "image": item[0][4],
      "price": item[0][5]
      }, 200

  """Endpoint for PUT requests. Edits a menu item"""
  @jwt_required
  def put(self, item_id):
    current_user = get_jwt_identity()
    role = current_user[2]
    if role == 1:
      item = item_id
      args = parser.parse_args()
      if len(check_valid(self)) == 0:
        MenuModel.update_menu_item(self, create_menu(self), item)
        return {"Success":"Menu has been updated"}, 200
      return check_valid(self)
    else:
      return {"Error":"Only admins are allowed to edit this"}, 401

  """Endpoint for DELETE requests. Deletes a menu item"""
  @jwt_required
  def delete(self, item_id):
    current_user = get_jwt_identity()
    if current_user[2] == 1:
      item = item_id
      MenuModel.delete_menu_item(self, item)
      return {"Success":"Menu has been deleted"}, 200
    else:
      return {"Error":"Only admins are allowed to delete a menu item"}, 401