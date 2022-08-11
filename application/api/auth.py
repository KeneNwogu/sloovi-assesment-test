from functools import wraps

import jwt
from bson import ObjectId
from flask import request, abort

from application import app, mongo
from application.api.errors import bad_request


def login_required(f):
    @wraps(f)
    def check_user_is_logged(*args, **kwargs):
        jwt_cookie = request.headers.get('Authorization', '').split()

        if len(jwt_cookie) != 2:
            return bad_request(f"Invalid Token provided")

        bearer, token = jwt_cookie
        if bearer.lower() != 'bearer':
            return bad_request(f"Invalid Token provided")

        if bearer:
            try:
                user_payload = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError,
                    jwt.exceptions.DecodeError) as e:
                return bad_request(f"Invalid or expired authentication token. Token: {jwt_cookie}")
            else:
                user = mongo.db.users.find_one({"_id": ObjectId(user_payload['user_id'])})
                return f(user, *args, **kwargs)

    return check_user_is_logged

