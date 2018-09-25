
from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity,
)


users = [
]


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True, help='please enter a username',  location='json')
parser.add_argument('password', type=str,
  help='password can\'t be empty', required=True, location='json')
parser.add_argument('access_token', location='json')

class Reg(Resource):
  """Endpoint to register a new user"""
  def post(self):
    args = parser.parse_args()
    username = args['username']
    password = args['password']

    user = [user for user in users if user['username'] == username]
    if len(user) != 0:
      return {'Error':'Username already exists'}, 400
    if username == "":
      return {'Error':'Please input a valid username'}, 400
    if password == "":
      return {'Error':'Please input a valid password'}, 400
    new_user = {
            'id': len(users) + 1,
            'username': username,
            'password': password
            }
    users.append(new_user)
    return {'users': users}, 200
  # @jwt_required
  def get(self):
    return {'message':'hey'}, 203

class Login(Resource):
  """Endpoint to login a user and create an access token"""
  def post(self):
    args = parser.parse_args()
    username = args['username']
    password = args['password']

    user = [user for user in users if user['username'] == username]
    if len(user) == 0:
      return {'Error':'Username does not exist'}, 404


    if password != user[0]['password']:
      return {'Error':'Wrong password'}, 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    current_user = get_jwt_identity()

    mesg = {
        'message': 'Logged in as {}'.format(current_user),
        'access_token': access_token,
        'refresh_token': refresh_token
        }
    return mesg, 200


class Refresh(Resource):
  """Endpoint to create Refresh tokens. It is not to be accessed externally"""
  @jwt_refresh_token_required
  def post(self):
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    mesg = {
      'access_token': access_token
    }
    return mesg, 200
