import unittest
import os
import sys
import json

localPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, localPath + '/../../../')

from run import create_app


class ViewsTest(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.order = {"title": "edit2", "description": "Lorem ipsum", "price": 5}

  def test_order_creation(self):
    """ assert that you can't create a duplicate order (asserts tiltle must be unique) """
    self.client().post('/dann/api/v1/orders', json=self.order)
    response = self.client().post('/dann/api/v1/orders', json=self.order)
    self.assertEqual(response.status_code, 400)

  def test_get_all_orders(self):
    self.client().post('/dann/api/v1/orders', json=self.order)
    response = self.client().get('/dann/api/v1/')
    self.assertEqual(response.status_code, 200)

  def test_get_single_order(self):
    response = self.client().get('/dann/api/v1/orders/1')
    self.assertEqual(response.status_code, 200)

  def test_edit_an_order(self):
    self.client().post('/dann/api/v1/orders', json=self.order)
    response = self.client().put('/dann/api/v1/orders/1',
                                 json={"title": "testagain", "description": "Lorem ipsum", "price": 10})
    self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
  unittest.main()
