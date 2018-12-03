from flask import make_response
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask import Flask, session
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
JSON_MIME_TYPE = 'application/json'
client = MongoClient('mongodb://localhost:27017/')
db = client['Real_estate_manager']


def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE
    return make_response(data, status, headers)


def is_logged_in():
    if 'Username' in session:
        return True
    else:
        return False
