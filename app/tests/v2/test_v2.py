import json
import os
import sys
import unittest
from dotenv import load_dotenv

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.db import Db

class Apiv2Test(unittest.TestCase):
  """ Tests for api v2 endpoints """

  def setUp(self):
    self.app = create_app("testing")
    self.client = self.app.test_client
    self.test_user = { "first_name": "dan", "last_name": "rico", "username": "dancan",
                        "email": "dan@dan.com", "password": "Admintest1", "phone": "0798765432", "role":"user"}

    self.test_user4 = { "first_name": "new", "last_name": "user", "username": "dancan1", "email": "dan@dan.com", "password": "Admintest1", "phone": "0798765632", "role": 2}
    self.secret_admin = { "first_name": "admin", "last_name": "user", "username": "admin13", "email": "secret@admin.com", "password": "Admintest1", "phone": "0701234567", "role": 1}
    self.test_login = { "username": "guest", "password": "admintest"}
    self.order = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    self.menu = {"title": "nyam chom", "category": "meat", "description": "grilled meat", "image_url": "loading", "price": 500}
    self.menu2 = {"title": "pizza", "category": "meat", "description": "wheat", "image_url": "loading", "price": 5000}

    with self.app.app_context():
      # Db().drops()
      Db().creates()

  def test_add_new_user(self):
    response = self.client().post('/dann/api/v2/signup', json=self.secret_admin)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)

  # def test_get_menu(self):
  #   response = self.client().get('/dann/api/v2/menu')
  #   json_data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)

  def test_user_reg(self):
    """ test user registration with valid credentials """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest1",
                        "email": "guest@dan.com", "password": "Guest12", "phone": "0798765431"}
    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)

  def test_admin_creation(self):
    """ test user registration with valid credentials """
    response = self.client().put('/dann/api/v2/signup', json={"password":"mysecret!"})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('mess'))
    self.assertEqual(json_data.get("mess"), "alert!!! admin created!")
    self.assertEqual(response.status_code, 200)

  def test_user_reg_with_no_username(self):
    """ test user registration with null username """
    test_user9 = { "first_name": "guest", "last_name": "user", "username": "",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user9)
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_email(self):
    """ test user registration with null email """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "", "password": "guest", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_password(self):
    """ test user registration with null password """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "guest@dan.com", "password": "", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    self.assertEqual(response.status_code, 400)


  def test_user_login(self):
    """ test user login """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('access_token'))
    self.assertEqual(response.status_code, 200)

  def test_user_login_with_wrong_password(self):
    """ test user login with wrong password """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "guest@dan.com", "password": "wrong", "phone": "0798765431"}
    response = self.client().post('/dann/api/v2/login', json=test_user2)
    self.assertNotEqual(response.status_code, 200)

  def test_user_login_with_wrong_username_and_email(self):
    """ test user login with wrong username """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "wrong",
                        "email": "wrong@dan.com", "password": "guest", "phone": "0798765431"}
    response = self.client().post('/dann/api/v2/login', json=test_user2)
    self.assertNotEqual(response.status_code, 200)

  def test_access_protected_endpoint_without_authorization(self):
    response = self.client().get('/dann/api/v2/signup')
    self.assertNotEqual(response.status_code, 200)



  # def test_get_the_menu(self):
  #   response = self.client().get('/dann/api/v2/menu')
  #   self.assertEqual(response.status_code, 200)

  def test_order_non_existent_item(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {}
    response = self.client().post('/dann/api/v2/users/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    self.assertEqual(response.status_code, 400)

  # def test_get_user_order(self):
  #   self.client().post('/dann/api/v2/signup', json=self.test_user)
  #   response = self.client().post('/dann/api/v2/login', json=self.test_user)
  #   json_data = json.loads(response.data)
  #   access_token = json_data.get('access_token')
  #   order2 = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
  #   self.client().get('/dann/api/v2/user/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
  #   response = self.client().get('/dann/api/v2/users/orders',headers={"Authorization":"Bearer " + access_token})
  #   self.assertEqual(response.status_code, 200)



  def tearDown(self):
    with self.app.app_context():
      Db().drops()
      # Db().creates()


if __name__ == '__main__':
  unittest.main()