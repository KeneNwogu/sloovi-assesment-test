import datetime

import jwt
from flask import Blueprint, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from application import mongo, app
from application.api.errors import bad_request
from application.serializers import UserSerializer

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        user_schema = UserSerializer()
        try:
            user = user_schema.load(data)
        except ValidationError:
            return bad_request('Invalid user details were provided')

        if mongo.db.users.find_one({"email": data['email']}):
            return bad_request('please use a different email address')

        password_hash = generate_password_hash(data['password'])
        user['password'] = password_hash

        mongo.db.users.insert_one(user)
        return {
            "success": True,
            "message": "successfully registered user",
            "email": user.get('email')
        }


@users.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if 'email' not in data or 'password' not in data:
            return bad_request("Email or username not provided")
        email = data['email']
        password = data['password']
        user = mongo.db.users.find_one({"email": email})
        if user:
            if check_password_hash(user.get('password'), password):
                # perform login
                payload = {
                    "user_id": str(user.get('_id')),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=720),
                    'iat': datetime.datetime.utcnow()
                }
                # set jwt
                token = jwt.encode(payload, app.config['SECRET_KEY'], "HS256")
                data = {
                    "message": "successfully logged in user",
                    "token": token
                }
                return data
        return bad_request("Invalid email or password")
