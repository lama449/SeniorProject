#buildings.py
#Lists all buildings for a specified facility and creates new buildings
#Monica Mahon, 11/5/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId
from SeniorProject.resources.room import Room
from SeniorProject.user_check import *

db = database.conn_DB()

class Building(Resource):
    def get(self, f_id, b_id=None):  # return a list of rooms for building
        facilities = db.facilities
        buildings = db.buildings
        res = {
            'msg': [],
            'err': []
        }
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
                    res['err'].append('Invalid building')
                    return jsonify(res)
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)

    def post(self, f_id):
        facilities = db.facilities
        buildings = db.buildings
        res = {
            'msg': [],
            'err': []
        }
        if not check_admin(f_id):
            res['err'].append('You do not have the permissions to create a new building.')
            return jsonify(res)
        else:
            current_facility = facilities.find_one({'_id': ObjectId(f_id)})
            if current_facility:
                data = request.json
                if not data.get('name'):
                    res['err'].append('Missing Building Name')
                if not data.get('address_L1'):
                    res['err'].append('Missing Building Address Line')
                if not data.get('city'):
                    res['err'].append('Missing Building City')
                if not data.get('state'):
                    res['err'].append('Missing Building State')
                if not data.get('zip'):
                    res['err'].append('Missing Building Zip')
                if not data.get('country'):
                    res['err'].append('Missing Building Country')
                if not data.get('phone'):
                    res['err'].append('Missing Building Phone')
                if not data.get('description'):
                    res['err'].append('Missing Building Description')

                if res['err']:
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
                res['err'].append('Invalid facility')
                return jsonify(res)

    def put(self, f_id, b_id):
        data = request.json
        facilities = db.facilities
        buildings = db.buildings
        res = {
            'msg': [],
            'err': []
        }

        if not check_admin(f_id):
            res['err'].append('You do not have the permissions to create a new building.')
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

        if not check_admin(f_id):
            res['err'].append('You do not have the permissions to create a new building.')
            return jsonify(res)

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

