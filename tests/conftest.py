import jwt
import datetime
import pytest

from application import app, mongo


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    with app.test_client() as test_client:
        yield test_client
        mongo.db.users.drop()
        mongo.db.templates.drop()


@pytest.fixture(scope='module')
def headers():
    # create test user
    user = mongo.db.users.insert_one({'email': 'testuser@gmail.com', "first_name": "Test", "last_name": "Test"})
    payload = {
        "user_id": str(user.inserted_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        'iat': datetime.datetime.utcnow()
    }
    # set jwt
    secret = app.config.get('SECRET_KEY')
    token = jwt.encode(payload, secret, "HS256")
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    yield auth_headers
    mongo.db.users.drop()
