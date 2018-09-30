from dotenv import load_dotenv
import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app

load_dotenv('.env')


class Apiv1Test(unittest.TestCase):
  """ Tests for api endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.order = {"title": "edit2", "description": "Lorem ipsum", "price": 5}
    self.test_user = {"username": "dan", "email": "dan@dan.com", "password": "dann"}

  def tearDown(self):
    pass


  def test_user_reg(self):
    """ test user registration with valid credentials """
    test_user2 = {"username": "dan3", "email": "dan1@dan.com", "password": "dann3"}
    response = self.client().post('/dann/api/v1/reg', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('users'))
    self.assertEqual(response.status_code, 200)

  def test_user_reg_with_already_existing_username(self):
    """ test user registration with already registered username """
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/reg', json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 409)

  def test_user_reg_with_no_username(self):
    """ test user registration with null username """
    test_user2 = {"username": "", "email": "", "password": "dan"}
    response = self.client().post('/dann/api/v1/reg', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_password(self):
    """ test user registration with null password """
    test_user2 = {"username": "dan", "email": "dan@dan.com", "password": ""}

    response = self.client().post('/dann/api/v1/reg', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 409)


  def test_user_login(self):
    """ test user login """
    self.client().post('/dann/api/v1/register', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('access_token'))
    self.assertEqual(response.status_code, 200)

  def test_user_login_with_wrong_password(self):
    """ test user login with wring password """
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    test_user2 = {"username": "dan", "email": "dan@dan.com", "password": "wrong"}
    response = self.client().post('/dann/api/v1/login', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 401)

  def test_user_login_with_wrong_username(self):
    """ test user login with wrong username """
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    test_user2 = {"username": "wrong", "email": "wrong@dan.com", "password": "dann"}
    response = self.client().post('/dann/api/v1/login', json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 404)

  def test_access_protected_endpoint_without_authorization(self):
    response = self.client().post('/dann/api/v1/reg', json=self.test_user)
    self.assertNotEqual(response.status_code, 200)


  def test_access_protected_endpoint_with_authorization(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v1/home', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertEqual(json_data.get("message"), "Hello, there ;-)")
    self.assertEqual(response.status_code, 200)


  def test_order_creation_without_authentication(self):
    """ assert that you can't create an order without authentication(must be logged in) """
    self.client().post('/dann/api/v1/orders', json=self.order)
    response = self.client().post('/dann/api/v1/orders', json=self.order)
    self.assertNotEqual(response.status_code, 400)

  def test_order_creation_while_authenticated(self):
    """ assert that you can create an order when authenticated """
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {"title": "another", "description": "Lorem ipsum", "price": 5}
    response = self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)

  def test_create_an_order_with_existing_title(self):
    """ assert that you can't create a duplicate order (asserts title must be unique) """
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get("Error"))
    self.assertEqual(response.status_code, 409)

  def test_create_an_order_with_without_title(self):
    """ assert that you can't create an order without a title) """
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    order2 = {"title": "", "description": "Lorem ipsum", "price": 5}
    response = self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=order2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get("Error"))
    self.assertEqual(response.status_code, 400)


  def test_get_all_orders(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().get('/dann/api/v1/orders')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('orders'))
    self.assertEqual(response.status_code, 200)

  def test_get_a_single_order(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().get('/dann/api/v1/order/1')
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('order'))
    self.assertEqual(response.status_code, 200)


  def test_get_a_non_existent_order(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    response = self.client().get('/dann/api/v1/order/0')
    self.assertEqual(response.status_code, 404)

  def test_to_edit_an_order_without_authentication(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"title": "testagain", "description": "Lorem ipsum", "price": 10}
    response = self.client().put('/dann/api/v1/order/1',
                                 json=data2)
    self.assertNotEqual(response.status_code, 201)

  def test_to_edit_an_order_with_authentication(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"title": "testagain", "description": "Lorem ipsum", "price": 10}
    response = self.client().put('/dann/api/v1/order/1',headers={"Authorization":"Bearer " + access_token}, json=data2)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('order'))
    self.assertEqual(response.status_code, 200)

  def test_edit_an_invalid_order(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"title": "testagain", "description": "Lorem ipsum", "price": 10}
    response = self.client().put('/dann/api/v1/order/0',headers={"Authorization":"Bearer " + access_token}, json=data2)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 404)

  def test_edit_an_order_with_invalid_data(self):
    self.client().post('/dann/api/v1/reg', json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/orders',headers={"Authorization":"Bearer " + access_token}, json=self.order)
    data2 = {"title": "", "description": "", "price": -4}
    response = self.client().put('/dann/api/v1/order/0',headers={"Authorization":"Bearer " + access_token}, json=data2)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
  unittest.main()
