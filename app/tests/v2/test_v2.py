import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.dbconn import *

class Apiv2Test(unittest.TestCase):
  """ Tests for api v2 endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.test_user = { "first_name": "dan", "last_name": "rico", "username": "dan",
                        "email": "dan@dan.com", "password": "dann", "phone": "0798765432"}
    self.order = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    self.menu = {"title": "nyam chom", "category": "meat", "description": "grilled meat", "image_url": "loading", "price": 500}

    with self.app.app_context():
      createtables('DBASE')


  # def test_connn(self):
    # conn = connect_db('DBASE')
    # cur = conn.cursor()
    # cur.execute(self.insertUserSQL, self.userData)
    # conn.commit()
    # cur.execute('select * from users')
    # rows = cur.fetchall()
    # for row in rows:
    #   print(row[2])
    # print("got it")


  def test_user_reg(self):
    """ test user registration with valid credentials """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}
    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)

    self.assertTrue(json_data.get('users'))
    self.assertEqual(response.status_code, 200)

  def test_user_reg_with_already_existing_username(self):
    """ test user registration with already registered username """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/signup', json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_username(self):
    """ test user registration with null username """
    test_user2 = { "first_name": "guest", "last_name": "user", "": "guest",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_password(self):
    """ test user registration with null password """
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "guest",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}

    response = self.client().post('/dann/api/v2/signup', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)


  def test_user_login(self):
    """ test user login """
    self.client().post('/dann/api/v1/register', json=self.test_user)
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
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 401)

  def test_user_login_with_wrong_username(self):
    """ test user login with wrong username """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    test_user2 = { "first_name": "guest", "last_name": "user", "username": "wrong",
                        "email": "guest@dan.com", "password": "guest", "phone": "0798765431"}
    response = self.client().post('/dann/api/v2/login', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 404)

  def test_access_protected_endpoint_without_authorization(self):
    response = self.client().post('/dann/api/v2/signup', json=self.test_user)
    self.assertNotEqual(response.status_code, 200)


  def test_access_protected_endpoint_with_authorization(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v2/home', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertEqual(json_data.get("message"), "Hello, there ;-)")
    self.assertEqual(response.status_code, 200)


  def test_order_creation_without_authentication(self):
    """ assert that you can't create an order without authentication(must be logged in) """
    self.client().post('/dann/api/v2/signup', json=self.order)
    response = self.client().post('/dann/api/v2/orders', json=self.order)
    self.assertNotEqual(response.status_code, 400)

  def test_order_creation_while_authenticated(self):
    """ assert that you can create an order when authenticated """
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    response = self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 201)

  # def test_create_an_order_with_existing_title(self):
  #   """ assert that you can't create a duplicate order (asserts title must be unique) """
  #   self.client().post('/dann/api/v2/signup', json=self.test_user)
  #   response = self.client().post('/dann/api/v2/login', json=self.test_user)
  #   json_data = json.loads(response.data)
  #   access_token = json_data.get('access_token')
  #   self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
  #   response = self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
  #   json_data = json.loads(response.data)
  #   self.assertTrue(json_data.get("Error"))
  #   self.assertEqual(response.status_code, 400)

  # def test_create_an_order_with_without_title(self):
  #   """ assert that you can't create an order without a title) """
  #   self.client().post('/dann/api/v2/signup', json=self.test_user)
  #   response = self.client().post('/dann/api/v2/login', json=self.test_user)
  #   json_data = json.loads(response.data)
  #   access_token = json_data.get('access_token')
  #   order2 = {"title": "", "description": "Lorem ipsum", "price": 5}
  #   response = self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
  #   json_data = json.loads(response.data)
  #   self.assertTrue(json_data.get("Error"))
  #   self.assertEqual(response.status_code, 400)


  def test_get_all_orders(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().get('/dann/api/v2/orders')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('orders'))
    self.assertEqual(response.status_code, 200)

  def test_get_a_single_order(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().get('/dann/api/v2/orders/1')
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('order'))
    self.assertEqual(response.status_code, 200)


  def test_get_a_non_existent_order(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().get('/dann/api/v2/orders/0')
    self.assertEqual(response.status_code, 404)

  def test_to_edit_an_order_without_authentication(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"price": 50, "description": "try edit", "ordered_by": "dan", "status": 0}
    response = self.client().put('/dann/api/v2/orders/1',
                                 json=data2)
    self.assertNotEqual(response.status_code, 201)

  def test_to_edit_an_order_with_authentication(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"price": 50, "description": "edited lorem", "ordered_by": "dan", "status": 0}
    response = self.client().put('/dann/api/v2/orders/1',headers={"Authorization":"Bearer " + access_token}, json=data2)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('order'))
    self.assertEqual(response.status_code, 201)

  def test_edit_an_invalid_order(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"price": 50, "description": "kila kitu hapa", "ordered_by": "dan", "status": 0}
    response = self.client().put('/dann/api/v2/orders/0',headers={"Authorization":"Bearer " + access_token}, json=data2)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_edit_an_order_with_invalid_data(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"price": "", "description": "", "ordered_by": "dan", "status": 0}
    response = self.client().put('/dann/api/v2/orders/1',headers={"Authorization":"Bearer " + access_token}, json=data2)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_get_the_menu(self):
    self.client().post('/dann/api/v2/signup', json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v2/menu',headers={"Authorization":"Bearer " + access_token}, json=self.menu)
    response = self.client().get('/dann/api/v2/menu')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('menu'))
    self.assertEqual(response.status_code, 200)



  def tearDown(self):
    with self.app.app_context():
      droptables('DBASE')

if __name__ == '__main__':
  unittest.main()
