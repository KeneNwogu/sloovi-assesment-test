import os

from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'test-secret-key'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI') or 'mongodb://127.0.0.1:27017/tweeter_test'
ma = Marshmallow(app)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.mp4', '.mp3'}
mongo = PyMongo()
CORS(app)

mongo.init_app(app)

from application.users.routes import users
from application.templates.routes import templates


app.register_blueprint(users)
app.register_blueprint(templates)



