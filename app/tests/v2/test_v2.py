import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.db import Db

class Apiv2Test(unittest.TestCase):
  """ Tests for api v2 endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.test_user = { "first_name": "dan", "last_name": "rico", "username": "dan",
                        "email": "dan@dan.com", "password": "dann", "phone": "0798765432", "role":"user"}

    self.test_user4 = { "first_name": "new", "last_name": "user", "username": "same", "email": "dan@dan.com", "password": "dann", "phone": "0798765632", "role":"user"}
    self.secret_admin = { "first_name": "admin1", "last_name": "user", "username": "admin1", "email": "secret@admin.com", "password": "admin", "phone": "0701234567", "role": "admin"}
    self.test_login = { "username": "guest", "password": "guest"}
    self.order = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    self.menu = {"title": "nyam chom", "category": "meat", "description": "grilled meat", "image_url": "loading", "price": 500}
    self.menu2 = {"title": "pizza", "category": "meat", "description": "wheat", "image_url": "loading", "price": 5000}

    with self.app.app_context():
      print("Hello")
      Db().drop()
      Db().create()

  def test_add_new_user(self):
    response = self.client().post('/dann/api/v2/signup', json=self.secret_admin)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)

  def test_get_menu(self):
    response = self.client().get('/dann/api/v2/menu')
    json_data = json.loads(response.data)
    # self.assertTrue(json_data.get('menu'))
    self.assertEqual(response.status_code, 200)

  def test_user_reg(self):
    """ test user registration with valid credentials """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}
    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)

    self.assertTrue(json_data.get('mess'))
    self.assertEqual(response.status_code, 200)

  def test_admin_creation(self):
    """ test user registration with valid credentials """
    response = self.client().put('/dann/api/v2/signup', json={"password":"mysecret!"})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('mess'))
    self.assertEqual(json_data.get("mess"), "alert!!! admin created!")
    self.assertEqual(response.status_code, 200)

  def test_user_reg_with_already_existing_username(self):
    """ test user registration with already registered username """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/signup', json=self.test_user)
    self.assertNotEqual(response.status_code, 200)

  def test_user_reg_with_already_existing_email(self):
    """ test user registration with already registered username """
    self.client().post('/dann/api/v2/signup', json=self.test_user4)
    response = self.client().post('/dann/api/v2/signup', json=self.test_user)
    self.assertNotEqual(response.status_code, 200)

  def test_user_reg_with_no_username(self):
    """ test user registration with null username """
    test_user9 = { "first_name": "guest", "last_name": "user", "username": "",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user9)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_email(self):
    """ test user registration with null email """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "", "password": "guest", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_password(self):
    """ test user registration with null password """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "guest@dan.com", "password": "", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
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


  def test_access_protected_endpoint_with_authorization(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertEqual(json_data.get("message"), "success")
    self.assertEqual(response.status_code, 200)


  def test_order_creation_without_authentication(self):
    """ assert that you can't create an order without authentication(must be logged in) """
    self.client().post('/dann/api/v2/signup', json=self.order)
    response = self.client().post('/dann/api/v2/orders', json=self.order)
    self.assertNotEqual(response.status_code, 400)


  def test_order_creation_with_admin_rights(self):
    """ assert that you can create an order when authenticated """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    response = self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)

  def test_get_the_menu(self):
    response = self.client().get('/dann/api/v2/menu')
    self.assertEqual(response.status_code, 200)

  def test_create_user_order(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    response = self.client().post('/dann/api/v2/users/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    # json_data = json.loads(response.data)
    # self.assertTrue(json_data.get("Success"))
    # self.assertEqual(json_data.get("Success"), "Order placed")
    self.assertEqual(response.status_code, 200)

  def test_get_user_order(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    self.client().get('/dann/api/v2/user/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    response = self.client().get('/dann/api/v2/users/orders',headers={"Authorization":"Bearer " + access_token})
    # json_data = json.loads(response.data)
    # self.assertTrue(json_data.get("My orders"))
    self.assertEqual(response.status_code, 200)

  def test_create_menu_item(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().post('/dann/api/v2/menu',headers={"Authorization":"Bearer " + access_token}, json=self.menu)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get("Mess"))
    self.assertEqual(json_data.get("Mess"), "Menu created sucessfully")
    self.assertEqual(response.status_code, 200)

  def test_user_edit_menu_item(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/menu', headers={"Authorization":"Bearer " + access_token}, json=self.menu)
    response = self.client().put('/dann/api/v2/menu/1', headers={"Authorization":"Bearer " + access_token}, json=self.menu2)

    self.assertEqual(response.status_code, 403)

  def test_admin_delete_menu_item(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/menu',headers={"Authorization":"Bearer " + access_token}, json=self.menu)
    self.client().delete('/dann/api/v2/menu/1',headers={"Authorization":"Bearer " + access_token})

    self.assertEqual(response.status_code, 200)



  def tearDown(self):
    with self.app.app_context():
      print('hey')
      Db().drop()
      Db().create()


if __name__ == '__main__':
  unittest.main()