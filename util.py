from flask import make_response
from pymongo import MongoClient

JSON_MIME_TYPE = 'application/json'
client = MongoClient('mongodb://localhost:27017/')
db = client['Real_estate_manager']

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE
    return make_response(data, status, headers)


def search_property(re_properties, property_id):
    for re_property in re_properties:
        if re_properties['id'] == property_id:
            return re_property
