import pytest

from app import app

@pytest.fixture
def app():
    return app

@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c