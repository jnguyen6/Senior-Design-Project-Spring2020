import pytest

@pytest.fixture
def resp(client):
    return client.get('/')

def test_hello_world(resp):
    assert resp.status_code == 200
