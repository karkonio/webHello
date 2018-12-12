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
    assert 'Hello' in response


def test_get_items(client):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = StringIO('{"test": 1}')
        response = client.get('/items')
        response = response.data.decode('utf-8')
        assert '<li>test: 1</li>' in response


def test_post_items(client):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = StringIO('{}')
        response = client.post(
            '/items',
            data={'item': 'test', 'quantity': 1}
        )
        response = response.data.decode('utf-8')
        assert '<li>test: 1</li>' in response
