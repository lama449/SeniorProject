#buildings.py
#Lists all buildings for a specified facility
#Monica Mahon, 11/5/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
# from bson.json_util import dumps
from SeniorProject import database

db = database.conn_DB()

class Building(Resource):
    def get(self, f_id, b_id=None):  # return a list of rooms for building
        facilities = db.facilities
        buildings = db.buildings
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if b_id is None:  
                current_buildings = buildings.find({'facilityID': current_facility.get('_id')})
                # convert the Cursor object to a dictionary so that it is JSON serializable
                current_buildings = [building for building in current_buildings]
                return jsonify(current_buildings)
            else:  # specific building
                current_building = buildings.find_one({'facilityID': current_facility.get('_id'), '_id': ObjectId(b_id)})
                if current_building:
                    return jsonify(current_building)
                    # return dumps(current_room)
                else:
                    return 'Invalid building'
        else:
            return 'Invalid facility'

    def post(self, f_id):
        facilities = db.facilities
        buildings = db.buildings
        data = request.form
        if not data.get('name'):
            return 'Missing Building Name'
        if not data.get('address_L1'):
            return 'Missing Building Address Line'
        if not data.get('city'):
            return 'Missing Building City'
        if not data.get('state'):
            return 'Missing Building State'
        if not data.get('zip'):
            return 'Missing Building Zip'
        if not data.get('country'):
            return 'Missing Building Country'
        if not data.get('phone'):
            return 'Missing Building Phone'
        if not data.get('description'):
            return 'Missing Building Description'
        takeID = buildings.insert_one({
        'name': data.get('name'),
        'address': {
            'address_L1': data.get('address_L1'),
            'address_L2': data.get('address_L2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'zip': data.get('zip'),
            'country': data.get('country')
            },
        'phone': data.get('phone'),
        'description': data.get('description'),
#        'presets': {},
#        'attributes': {},
#        'maintenance': {},
#        'groups': [{
#            '_id': ObjectId(),
#            'name': 'admin'
#            }]
        })
        return jsonify({'_id': takeID.inserted_id})

    def put(self):
        pass

    def delete(self):
        pass
