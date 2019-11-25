#buildings.py
#Lists all buildings for a specified facility and creates new buildings
#Monica Mahon, 11/5/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
# from bson.json_util import dumps
from SeniorProject import database
from bson.objectid import ObjectId
from SeniorProject.resources.room import Room

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
        users = db.users
        res = {
            'msg': [],
            'err': []
        }
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        groups = current_facility.get('groups')
        admin_id = next(g for g in groups if g['name'] == 'admin')['_id']
        current_user = users.find_one({'_id': ObjectId(session.get('user').get('_id')), 'groupID': ObjectId(admin_id)})
        if current_user is None:
            res['msg'].append('You do not have the permissions to create a new building.')
            return jsonify(res)
        else:
            if current_facility:
                data = request.json
                if not data.get('name'):
                    res['err'].append('Missing Building Name')
                    return jsonify(res)
                if not data.get('address_L1'):
                    res['err'].append('Missing Building Address Line')
                    return jsonify(res)
                if not data.get('city'):
                    res['err'].append('Missing Building City')
                    return jsonify(res)
                if not data.get('state'):
                    res['err'].append('Missing Building State')
                    return jsonify(res)
                if not data.get('zip'):
                    res['err'].append('Missing Building Zip')
                    return jsonify(res)
                if not data.get('country'):
                    res['err'].append('Missing Building Country')
                    return jsonify(res)
                if not data.get('phone'):
                    res['err'].append('Missing Building Phone')
                    return jsonify(res)
                if not data.get('description'):
                    res['err'].append('Missing Building Description')
                    return jsonify(res)
                takeID = buildings.insert_one({
                    'name': data.get('name'),
                    'address': {
                        'address_L1': data.get('address_L1'),
                        'address_L2': data.get('address_L2'),
                        'city': data.get('city'),
                        'state': data.get('state'),
                        'zip': data.get('zip'),
                        'country': data.get('country')},
                    'phone': data.get('phone'),
                    'description': data.get('description'),
                    'facilityID': ObjectId(f_id)
                })
                return jsonify({'_id': takeID.inserted_id})
            else:
                return jsonify(res['err'].append('Invalid facility'))

    def put(self, f_id, b_id):
        data = request.json
        facilities = db.facilities
        buildings = db.buildings
        users = db.users
        current_user = users.find_one({'_id': ObjectId(session.get('user').get('_id')), 'groupID.name': 'admin'})
        res = {
            'msg': [],
            'err': []
        }

        if current_user is None:
            res['msg'].append('You do not have the permissions to create a new building.')
            return jsonify(res)
        else:
            current_facility = facilities.find_one({'_id': ObjectId(f_id)})
            if current_facility:
                current_building = buildings.find_one({'_id': ObjectId(b_id)})
                if current_building:
                    updated_building = buildings.update_one({'_id': ObjectId(b_id)},
                                                            {'$set':
                                                                 {'name': data.get('name'),
                                                                  'address': {
                                                                      'address_L1': data.get('address_L1'),
                                                                      'address_L2': data.get('address_L2'),
                                                                      'city': data.get('city'),
                                                                      'state': data.get('state'),
                                                                      'zip': data.get('zip'),
                                                                      'country': data.get('country')},
                                                                  'phone': data.get('phone'),
                                                                  'description': data.get('description'),
                                                                  'facilityID': ObjectId(f_id)}
                                                             })
                    res['msg'].append('success')
                    return jsonify(res)
                else:
                    res['err'].append('Invalid building')
                    return jsonify(res) 
            else:
                res['err'].append('Invalid facility')
                return jsonify(res)

    def delete(self, f_id, b_id):
        res = {
            'msg': [],
            'err': []
        }
        facilities = db.facilities
        buildings = db.buildings
        rooms = db.rooms
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            current_building = buildings.find_one({'_id': ObjectId(b_id)})
            if current_building:
                drooms = rooms.find({'buildingID': ObjectId(b_id)})
                if drooms:
                    print(drooms)
                    for room in drooms:
                        Room().delete(f_id, b_id, str(room.get('_id')))
                elif drooms is None:
                    print('No rooms to delete')
                buildings.delete_one({'_id': ObjectId(b_id)})
                res['msg'].append('Building deleted')
                return jsonify(res)
            else:
                res['err'].append('Invalid building')
                return jsonify(res)
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)

