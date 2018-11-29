from flask import Flask, jsonify, request, Blueprint
from util import json_response, JSON_MIME_TYPE

properties_mgt_file = Blueprint('properties_mgt_file', __name__)

re_properties = [{
    'id': 1,
    'Name': 'Maxime BOUN',
    'Descrption': 'Small charming apartment with exposed beams, located in the 11th arrondissement of Paris',
    'Type': 'Apartment',
    'City': 'Paris',
    'Number of rooms': '2',
    'Rooms_features': [{'bedroom': 'Quiet and bright. There is a sofa bed (140x200)'}],
    'Landlord': 'Maxime BOUN'
}]


@properties_mgt_file.route('/')
def index():
    return "Test Arcane API Rest en Python"


@properties_mgt_file.route('/properties')
def re_properties_list():
    return jsonify(re_properties)


@properties_mgt_file.route('/createproperty', methods=['POST'])
def create_re_property():
    if request.content_type != JSON_MIME_TYPE:
        error = jsonify({'Error': 'Invalid Content-Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('id'), data.get('Name')]):
        error = jsonify({'Error': 'id/Name missing'})
        return json_response(error, 400)

    re_properties.append(data)

    return json_response(data='property added', status=200)
