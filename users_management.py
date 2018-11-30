from datetime import date
from flask import Flask, jsonify, request, Blueprint
from util import json_response, JSON_MIME_TYPE, db
from bson.json_util import dumps

user_mgt_file = Blueprint('user_mgt_file', __name__)

users_col = db['users']


@user_mgt_file.route('/users')
def show_users():
    all_users_req = users_col.find()
    return dumps(all_users_req)
    # use of dumps to convert a pymongo cursor to json


@user_mgt_file.route('/createuser', methods=['POST'])
def create_user():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('First name'), data.get('Last name')]):
        error = jsonify({'Error': 'First/last name missing'})
        return json_response(error, 400)

    users_col.insert(data)
    return json_response(data='User added', status=200)


@user_mgt_file.route('/edituser', methods=['POST'])
def edit_user():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = dict(request.json)

    if 'id' not in data:
        error = jsonify({'Error': 'id missing'})
        return json_response(error, 400)
    else:
        property_id = data['id']

    data.pop('id', None)
    new_values = {'$set': data}
    users_col.update_one({'id': property_id}, new_values)
    return json_response(data='user updated', status=200)
