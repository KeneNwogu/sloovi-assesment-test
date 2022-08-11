import json
from application import mongo


def test_valid_registration(client, headers):
    data = {
        "first_name": "lead_test@subi.com",
        "last_name": "123456",
        "email": "lead_test@subi.com",
        "password": "123456"
    }
    response = client.post('/register', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 200


def test_invalid_registration(client):
    data_with_missing_field = {
        "first_name": "lead_test@subi.com",
        "last_name": "123456",
        "email": "lead_test@subi.com",
    }
    response = client.post('/register', headers={'Content-Type': 'application/json'},
                           data=json.dumps(data_with_missing_field))
    assert response.status_code == 400


def test_login(client):
    data = {
        "email": "lead_test@subi.com",
        "password": "123456"
    }
    user = mongo.db.users.insert_one(data)
    data.pop('_id')
    response = client.post('/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 200
    mongo.db.users.drop()


def test_invalid_login(client):
    data = {
        "email": "invalid_login_test@subi.com",
        "password": "123456"
    }
    response = client.post('/login', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 400
