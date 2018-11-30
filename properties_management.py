from flask import Flask, jsonify, request, Blueprint
from util import json_response, JSON_MIME_TYPE, db
from bson.json_util import dumps

properties_mgt_file = Blueprint('properties_mgt_file', __name__)
properties_col = db['re_properties']

@properties_mgt_file.route('/')
def index():
    return 'Test Arcane'


@properties_mgt_file.route('/properties')
def re_properties_list():
    all_properties_req = properties_col.find()
    if all_properties_req is None:
        error = jsonify({'Error': 'No properties'})
        return json_response(error, 400)
    return dumps(all_properties_req)  # use of dumps to convert a pymongo cursor to json


@properties_mgt_file.route('/createproperty', methods=['POST'])
def create_re_property():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('id'), data.get('Name')]):
        error = jsonify({'Error': 'id/Name missing'})
        return json_response(error, 400)

    properties_col.insert(data)
    return json_response(data='property added', status=200)


@properties_mgt_file.route('/editproperty', methods=['POST'])
def edit_property():
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
    properties_col.update_one({'id': property_id}, new_values)
    return json_response(data='property updated', status=200)


@properties_mgt_file.route('/deleteproperty/<string:property_id>', methods=['GET'])
def delete(property_id):
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not data.get('id'):
        error = jsonify({'Error': 'id missing'})
        return json_response(error, 400)

    properties_col.delete_one({'id': property_id})
    return json_response(data='property ' + property_id + ' deleted', status=200)
