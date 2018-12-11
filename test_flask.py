import pytest

from io import StringIO
from unittest import mock

from hello import app # из файла hello.py 


@pytest.fixture
def client():
    client = app.test_client() # для обнаружения пайтестом
    return client


def test_index(client): # первый текст для проверки корневого адреса
    response = client.get('/')
    response = response.data.decode('utf-8') # для нормальной презентации содержимого
    assert 'Hello' in response


def test_index(client): # второй assert для проверки что по адресу ip/items записан словарь
    with mock.patch('hello.open') as mocked: # open as очень сложный, поэтому используем для открытия БД mock
        mocked.return_value = StringIO('{"test": 1}') # описываем какого формата должны быть данные в .html
        response = client.get('/items')
        response = response.data.decode('utf-8')
        assert '<li>test: 1</li>' in response
