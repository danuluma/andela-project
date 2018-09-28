from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity,
)

import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.dbconn import *



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
  help='role can\'t be empty', required=True, location='json')
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
    role = args['role']

    if username == "":
      return {'Error':'Please input a valid username'}, 400
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

    insertsql = """
    INSERT INTO users (first_name, last_name, username, email, password, phone, role)
    VALUES (%s,%s,%s,%s,%s,%s,%s);
    """
    mydb = 'DBASE'
    conn = connect_db(mydb)
    cur = conn.cursor()
    try:
      cur.execute(insertsql, new_user)
      conn.commit()
    except:
      return{'Error': 'sorry invalid data'}, 500
    cur.execute('select * from users')
    rows = cur.fetchall()
    users = []
    for row in rows:
      print(row)
      user = {'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'email': row[4], 'password': row[5], 'phone': row[6], 'role': row[7]}
      users.append(user)

    return {'users': users}, 200

  # @jwt_required
  def get(self):
    return {'message':'hey'}, 203

class Loginv2(Resource):
  """Endpoint to login a user and create an access token"""
  def post(self):
    args = parser.parse_args()
    username = args['username']
    password = args['password']

    selectsql = """SELECT * FROM users WHERE username='{0}'""".format(username)
    mydb = 'DBASE'
    conn = connect_db(mydb)
    cur = conn.cursor()
    cur.execute(selectsql)
    user = cur.fetchone()

    if password == user[5]:
      access_token = create_access_token(identity=username)
      refresh_token = create_refresh_token(identity=username)
      current_user = get_jwt_identity()

      mesg = {
          'message': 'Logged in as {}'.format(current_user),
          'access_token': access_token,
          'refresh_token': refresh_token
          }
      return mesg, 200
    else:
      return {'Error': 'Wrong password'}, 200


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
