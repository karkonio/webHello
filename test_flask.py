from hello import app


def test_index():
    client = app.test_client()
    response = client.get('/')
    response = response.data.decode('utf-8')
    assert 'Hello' in response