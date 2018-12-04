from flask import Flask, jsonify, request, Blueprint, session
from util import json_response, JSON_MIME_TYPE, db, bcrypt, is_logged_in
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.json_util import dumps


user_mgt_file = Blueprint('user_mgt_file', __name__)

users_col = db['users']


@user_mgt_file.route('/users')
def show_users():
    all_users_req = users_col.find()
    return dumps(all_users_req)
    # use of dumps to convert a pymongo cursor to json


@user_mgt_file.route('/edituser', methods=['POST'])
def edit_user():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = dict(request.json)

    if is_logged_in():
        # the user can only change his data and needs to be logged in
        if 'Password' in data:
            # hash the new password
            data['Password'] = bcrypt.generate_password_hash(data['Password']).decode('utf-8')
        new_values = {'$set': data}
        users_col.update_one({'_id': ObjectId(session['user_id'])}, new_values)
        return json_response(data=jsonify({'Success': 'User edited'}), status=200)
    else:
        return json_response(data=jsonify({'Error': 'you are not logged in'}), status=400)


@user_mgt_file.route('/register', methods=['GET', 'POST'])
def register():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('First Name'), data.get('Last Name'), data.get('Username'), data.get('Password')]):
        error = jsonify({'Error': 'field(s) missing'})
        return json_response(error, 400)
    hashed_password = bcrypt.generate_password_hash(data.get('Password')).decode('utf-8')
    data['Password'] = hashed_password

    try:
        users_col.insert(data)
    except DuplicateKeyError:
        error = jsonify({'Error': 'Username already exists'})
        return json_response(error, 400)

    return json_response(data=jsonify({'Success': 'User added'}), status=200)


@user_mgt_file.route('/login', methods=['GET', 'POST'])
def login():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('Username'), data.get('Password')]):
        error = jsonify({'Error': 'username/password missing'})
        return json_response(error, 400)

    user_in_db = users_col.find({'Username': data.get('Username')})

    for user in user_in_db:
        # iterate over the pymongo cursor
        user_id = user['_id']
        hashed_password = user['Password']
        Full_name = user['First name'] + ' ' + user['Last name']

    if user_in_db.count() != 0 and bcrypt.check_password_hash(hashed_password, data.get('Password')):
        # Store the user information into the session
        session.clear()
        session['user_id'] = str(user_id)
        session['Username'] = data.get('Username')
        session['Full name'] = Full_name
        return json_response(data=jsonify({'Response': 'You are connected as ' + session['Username']}), status=200)
    else:
        error = jsonify({'Error': 'bad username/password'})
        return json_response(error, 400)


@user_mgt_file.route('/logout')
def logout():
    # remove the username from the session if it's there
    if is_logged_in():
        session.pop('Username', None)
        session.pop('Full name', None)
        return json_response(jsonify({'Success': 'Logged out'}), 400)
    else:
        error = jsonify({'Error': 'you are not logged in'})
        return json_response(error, 400)
