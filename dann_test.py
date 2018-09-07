import json
import pytest
from app import app


@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client


def post_json(client, url, data):
    """Send data as json to the specified url """
    return client.post(url, data=json.dumps(data), content_type='application/json')


def put_json(client, url, data):
    """Send data as json to the specified url """
    return client.put(url, data=json.dumps(data), content_type='application/json')


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


def test_home(client):
    response = client.get('/')
    assert b'Hi person ;-)' in response.data


def test_get_all(client):
    response = client.get('/dann/api/v1/orders')
    assert response.status_code == 200


def test_get_order1(client):
    response = client.get('/dann/api/v1/orders/1')
    assert response.status_code == 200
    response = client.get('/dann/api/v1/orders/999')
    assert response.status_code == 404


def test_create_order(client):
    response = post_json(client, '/dann/api/v1/orders', {'': ''})
    assert response.status_code == 404
    response = post_json(client, '/dann/api/v1/orders', {'title': 'burger'})
    assert response.status_code == 201


def test_edit_order(client):
    response = put_json(client, '/dann/api/v1.0/orders/1', {'': ''})
    assert response.status_code == 404
    response = put_json(client, '/dann/api/v1.0/orders/1', {'price': 50})
    # assert response.status_code == 201
