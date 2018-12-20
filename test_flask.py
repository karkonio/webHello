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
            '/items', data={})
        response = response.data.decode('utf-8')
        assert '<input type="submit" value="Update">' in response
