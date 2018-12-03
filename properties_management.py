from flask import Flask, jsonify, request, Blueprint, session
from util import json_response, JSON_MIME_TYPE, db, is_logged_in
from bson.json_util import dumps

properties_mgt_file = Blueprint('properties_mgt_file', __name__)
properties_col = db['re_properties']


@properties_mgt_file.route('/')
def index():
    return 'Test Arcane'


@properties_mgt_file.route('/properties', methods=['GET'])
# lists all the properties from all the cities
def re_properties_list():
    all_properties_req = properties_col.find()
    if all_properties_req is None:
        error = jsonify({'Error': 'No properties'})
        return json_response(error, 400)
    return dumps(all_properties_req)  # use of dumps to convert a pymongo cursor to json


@properties_mgt_file.route('/cityproperties', methods=['POST'])
# lists all the properties from one city in particular: expects a POST request in a application/json Content-Type
# with at least an 'id' field
def re_properties_by_city():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if data.get('city') is None:
        error = jsonify({'Error': 'city missing'})
        return json_response(error, 400)
    else:
        property_req = properties_col.find({'City': data.get('city')})
        if (property_req.count() == 0):
            error = jsonify({'Error': 'No property found'})
            return json_response(error, 400)
        return json_response(dumps(property_req), status=200)


@properties_mgt_file.route('/createproperty', methods=['POST'])
# creates a city: expects a POST request in a application/json Content-Type
# with at least 'Name' field
def create_re_property():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('Name')]):
        error = jsonify({'Error': 'Name missing'})
        return json_response(error, 400)

    properties_col.insert(data)
    return json_response(data='property added', status=200)


@properties_mgt_file.route('/editproperty', methods=['POST'])
def edit_re_property():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    if is_logged_in():
        print(session['Full name'])
        data = dict(request.json)
        new_values = {'$set': data}
        properties_col.update_one({'Landlord': session['Full name']}, new_values)
        return json_response(data=jsonify({'success': 'property updated'}), status=200)

    else:
        return json_response(data=jsonify({'error': 'Please log in first!'}), status=400)


@properties_mgt_file.route('/deleteproperty/', methods=['GET'])
def delete_re_property():
    if is_logged_in():
        properties_col.delete_one({'Landlord': session['Full name']})
        return json_response(data=jsonify({'success': 'property deleted'}), status=200)

    else:
        return json_response(data=jsonify({'error': 'Please log in first!'}), status=400)
