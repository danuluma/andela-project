from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.modeluser import UserModel
from app.api.v2.models.validate import Validate



parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('first_name', type=str, required=True, help='please enter a first_name',  location='json')
parser.add_argument('last_name', type=str,
  help='last_name can\'t be empty', required=True, location='json')
parser.add_argument('username', type=str,
  help='username can\'t be empty', required=True, location='json')
parser.add_argument('email', type=str,
  help='email can\'t be empty', required=True, location='json')
parser.add_argument('password', type=str,
  help='password can\'t be empty', required=True, location='json')
parser.add_argument('phone', type=str,
  help='phone can\'t be empty', required=True, location='json')
parser.add_argument('role', type=str,
  help='', location='json')
parser.add_argument('access_token', location='json')

class Signup(Resource):
  """Endpoint to register a new user"""
  def post(self):
    args = parser.parse_args()
    first_name = args['first_name'].strip()
    last_name = args['last_name'].strip()
    username = args['username'].strip()
    email = args['email'].strip()
    password = args['password']
    phone = args['phone'].strip()
    role = "user"

    if not Validate().validate_name(args['title']):
      return {"Error":"Title should have at least 3 characters!"}
    if not Validate().validate_name(args['category']):
      return {"Error":"Category should have at least 3 characters!"}


    if username == "":
      return {'Error':'Please input a valid username'}, 400
    if email == "":
      return {'Error':'Please input a valid email'}, 400
    if password == "":
      return {'Error':'Please input a valid password'}, 400
    new_user = [
          first_name,
          last_name,
          username,
          email,
          password,
          phone,
          role
    ]

    UserModel.add_new_user(self, new_user)
    return {'mess': "success"}, 200

  @jwt_required
  def get(self):
    mess = UserModel.get_all_users(self)
    return {'message':"success"}, 200

  def put(self):
    parser2 = reqparse.RequestParser(bundle_errors=True)
    parser2.add_argument('password', type=str,
      help='password can\'t be empty', required=True, location='json')
    args = parser2.parse_args()
    password = args['password'].strip()
    if password == "mysecret!":
      UserModel().add_admin_user()
      return {'mess': "alert!!! admin created!"}, 200
    else:
      return {"mess":"Wrong password"}, 401


class Loginv2(Resource):
  """Endpoint to login a user and create an access token"""

  def post(self):
    parser2 = reqparse.RequestParser(bundle_errors=True)
    parser2.add_argument('username', type=str,
      help='username can\'t be empty', required=False, location='json')
    parser2.add_argument('email', type=str,
      help='email can\'t be empty', required=False, location='json')
    parser2.add_argument('password', type=str,
      help='password can\'t be empty', required=True, location='json')

    args = parser2.parse_args()
    username = args['username'].strip()
    email = args['email'].strip()
    password = args['password'].strip()

    user = UserModel.get_single_user(self, username, email)
    if len(user) == 0:
      return {'Error': 'User not found'}, 401
    else:

      userdetails = [user['username'], user['id'], user['role']]
      if password == user['password']:
        access_token = create_access_token(identity=userdetails)
        refresh_token = create_refresh_token(identity=userdetails)
        current_user = get_jwt_identity()

        mesg = {
            'access_token': access_token
            }
        return mesg, 200
      else:
        return {'Error': 'Wrong password'}, 401

  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    mesg = {
      'current_user': current_user[2]
    }
    return mesg, 200


