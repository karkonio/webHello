import json
import pytest
from io import StringIO
from unittest import mock
from hello import app


@pytest.fixture
def client():
    client = app.test_client()
    return client


def test_index(client):
    response = client.get('/')
    response = response.data.decode('utf-8')
    assert 'Hello, my dear customer.' in response


def test_get_items(client):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = StringIO('{"test": 1}')
        response = client.get('/items')
        response = response.data.decode('utf-8')
        assert 'value="test"' and 'value="1"' in response


def test_post_items_update(client):
    with mock.patch('hello.open') as mocked:
        cart = {
            'banana': 5,
            'grapes': 100
        }
        mocked.return_value = StringIO(json.dumps(cart))
        response = client.post(
            '/items',
            data={
                'banana': 'banana',
                'banana_quantity': 5,
                'grapes': 'apple',
                'grapes_quantity': 100
            }
        )
        response = response.data.decode('utf-8')
        assert '<input type="text" value="banana" name="banana">' in response
        assert '<input type="text" value="5" name="banana_quantity">' \
            in response
        assert '<input type="text" value="apple" name="apple">' in response
        assert '<input type="text" value="100" name="apple_quantity">' \
            in response


def test_post_items_add(client):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = StringIO('{"_": 0}')
        response = client.post(
            '/items',
            data={'{{ item }}': 'test', '{{ item }}_quantity': '1'}
        )
        response = response.data.decode('utf-8')
        assert 'value="test"' and 'value="1"' in response


def test_post_items_remove(client):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = StringIO('{"test": 1}')
        response = client.post(
            '/items', data={

            }
        )
        response = response.data.decode('utf-8')
        assert '<input type="submit" value="Update">' in response
