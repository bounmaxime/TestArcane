from datetime import date
from flask import Flask, jsonify, request, Blueprint
from util import json_response, JSON_MIME_TYPE

user_mgt_file = Blueprint('user_mgt_file', __name__)

user_list = [{
    'First name': 'Maxime',
    'Last name': 'BOUN',
    'Date of birth': date(day=28, month=8, year=1996)
}]


@user_mgt_file.route('/users')
def show_users():
    return jsonify(user_list)


@user_mgt_file.route('/createuser', methods=['POST'])
def create_user():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('First name'), data.get('Last name')]):
        error = jsonify({'Error': 'First/last name missing'})
        return json_response(error, 400)

    user_list.append(data)

    return json_response(data='User added', status=200)
