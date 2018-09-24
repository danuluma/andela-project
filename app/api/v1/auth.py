
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
parser.add_argument('username', type=str, location='json')
parser.add_argument('password', type=str,
  help='pword can\'t be empty', required=True, location='json')
parser.add_argument('access_token', location='json')

class Reg(Resource):
  """docstring for Reg"""
  def post(self):
    args = parser.parse_args()
    use = {
            'id': len(users) + 1,
            'username': args['username'],
            'password': args['password']
            }
    users.append(use)
    return {'users': users}

  def get(self):
    return {'message':'hey'}, 200

class Login(Resource):
  """docstring for Login"""
  def post(self):
    args = parser.parse_args()
    username = args['username']
    password = args['password']

    user = [user for user in users if user['username'] == username]
    if len(user) == 0:
      return {'Error':'Username does not exist'}, 404


    if args['password'] != user[0]['password']:
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
  """docstring for Refresh"""
  @jwt_refresh_token_required
  def post(self):
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    mesg = {
      'access_token': access_token
    }
    return mesg, 200
