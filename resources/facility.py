from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
from bson.objectid import ObjectId
import bcrypt
import string
import random
from SeniorProject import database

db = database.conn_DB()

class Facility(Resource):
    def get(self, f_id):
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            return jsonify(current_facility)
        else:
            return 'Invalid facility'

    def post(self):
        facilities = db.facilities
        data = request.form
        if data.get('access_code'):
            return jsonify(facilities.find_one({'access_code': data.get('access_code')}))
        while data.get('private') == 'true':
            access_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            check_facility = facilities.find_one({'access_code': access_code})
            if check_facility is None:
                break
        takeID = facilities.insert_one({
        'name': data.get('name'),
        'private': data.get('private') == 'true',
        'access_code': access_code if (data.get('private') == 'true') else '',              
        'address': [{
            'address_L1': data.get('address_L1'),
            'address_L2': data.get('address_L2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'zip': data.get('zip'),
            'country': data.get('country')
            }],
        'phone': data.get('phone'),
        'description': data.get('description'),
        'presets': {},
        'attributes': {},
        'maintenance': {},
        'groups': [{
            '_id': ObjectId(),
            'name': 'admin'
            }]
        })
        return jsonify({'_id': takeID.inserted_id})

    def put(self):
        pass

    def delete(self):
        pass
