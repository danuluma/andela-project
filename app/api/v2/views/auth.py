from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import psycopg2
import psycopg2.extras

import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.modeluser import UserModel
from app.api.v2.models.validate import Validate



parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('first_name', type=str, location='json')
parser.add_argument('last_name', type=str, location='json')
parser.add_argument('username', type=str, location='json')
parser.add_argument('email', type=str, location='json')
parser.add_argument('password', type=str, location='json')
parser.add_argument('phone', type=str, location='json')
parser.add_argument('role', type=str, location='json')
parser.add_argument('access_token', location='json')

class Signup(Resource):
  """Endpoint to register a new user"""
  def post(self):
    args = parser.parse_args()
    first_name = args['first_name']
    last_name = args['last_name']
    username = args['username']
    email = args['email']
    password = args['password']
    phone = args['phone']
    role = 2

    errors = []
    if not Validate().validate_name(first_name):
      errors.append({"Error":"Name should have at least 3 characters!"})

    if not Validate().validate_name(last_name):
      errors.append({"Error":"Name should have at least 3 characters!"})

    if not Validate().validate_username(username):
      errors.append({"Error":"Username should have between 5-10 characters!"})

    if not Validate().validate_email(email):
      errors.append({"Error":"Enter a valid email"})

    if not Validate().validate_password(password):
      errors.append({"Error":"Password should have 6-12 characters and contain only letters and numbers"})

    if not Validate().validate_phone(phone):
      errors.append({"Error":"Phone number should have 10-12 digits"})

    if len(errors) != 0:
      return errors, 400

    new_user = [
          first_name,
          last_name,
          username,
          email,
          password,
          phone,
          role
    ]
    try:
      UserModel.add_new_user(self, new_user)
      return {'mess': "success"}, 200

    except psycopg2.IntegrityError:
      return {"Error":"Data already exists"}, 409

  @jwt_required
  def get(self):
    mess = UserModel.get_all_users(self)
    return {'message': mess}, 200


class Loginv2(Resource):
  """Endpoint to login a user and create an access token"""

  def post(self):
    args = parser.parse_args()
    username = args['username']
    email = args['email']
    password = args['password']

    errorl = []
    if not Validate().validate_username(username):
      errorl.append({"Error":"Username should have between 5-10 characters!"})

    if not Validate().validate_email(email):
      errorl.append({"Error":"Enter a valid email"})

    if not Validate().validate_password(password):
      errorl.append({"Error":"Password should have 6-12 characters"})

    if len(errorl) != 0:
      return errorl, 400

    user = UserModel.get_single_user(self, username, email)
    if len(user) == 0:
      return {'Error': 'User not found'}, 404
    else:
      u_id = user[0][0]
      u_username = user[0][3]
      u_role = user[0][7]
      u_password = user[0][5]

      userdetails = [u_id, u_username, u_role]
      if password == u_password:
        access_token = create_access_token(identity=userdetails, expires_delta=False)
        current_user = get_jwt_identity()

        mesg = {
            'access_token': access_token
            }
        return mesg, 200
      else:
        return {'Error': 'Wrong details'}, 401

