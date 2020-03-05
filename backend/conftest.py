import pytest

from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    db.drop_all()
    db.create_all()
    with app.test_client() as client:
        yield client