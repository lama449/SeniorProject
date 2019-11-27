from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from bson.objectid import ObjectId
#from bson.json_util import dumps
from SeniorProject import database
from SeniorProject.resources.maintenance import Maintenance

db = database.conn_DB()

class Room(Resource):
    def get(self, f_id, b_id, r_id=None): # return a list of rooms for building
        
        validation = validate_room(f_id, b_id, r_id)
        if validation[0] is True:
            rooms = db.rooms
            if r_id is None:  # return list of rooms for building
                current_building = validation[1]
                current_rooms = rooms.find({'buildingID': current_building.get('_id')})
                # convert the Cursor object to a dictionary so that it is JSON serializable
                current_rooms = [room for room in current_rooms]
                return jsonify(current_rooms)
            else:  # specific room
                current_room = validation[1]
                if current_room:
                    return jsonify(current_room)
                else:
                    return {'err': 'Invalid room'}
        else:
            return {'err': validation[1]}


    def post(self, f_id, b_id):
        res =   {
                'msg': [],
                'err': []
                }
              
        data = request.json
        if not data.get('name'):
            res['err'].append('Missing name')
        if not data.get('capacity'):
            res['err'].apppend('Missing room capacity')
        if not data.get('number'):
            res['err'].append('Missing room number')
        if res['err']:
            return jsonify(res)
        
        validation = validate_room(f_id, b_id)
        if validation[0] is True:
            rooms = db.rooms
            current_building = validation[1]
                               
            takeID = rooms.insert_one({
            'attributes': data.get('attributes'),
            'buildingID' : current_building.get('_id'),
            'capacity': data.get('capacity'),
            'groupID': data.get('groupID'),
            'name': data.get('name'),
            'number': data.get('number'),
            'reservations': []
            })
            return jsonify({'_id': takeID.inserted_id})
        else:
            return {'err': validation[1]}


    def put(self, f_id, b_id, r_id):
        data = request.json
        rooms = db.rooms
        
        validation = validate_room(f_id, b_id, r_id)
        if validation[0] is True:
            updated_room = rooms.update_one({'_id': ObjectId(r_id)}, 
            {'$set': {'number': data.get('number'),
            'name': data.get('name'),
            'capacity': data.get('capacity'),
            'attributes': {data.get('attributes')}, 
            'groupID': data.get('groupID')}})
        else:
            return {'err': validation[1]}


    def delete(self, f_id, b_id, r_id):
        validation = validate_room(f_id, b_id, r_id)
        if validation[0] is True:
            rooms = db.rooms
            Maintenance().delete(f_id, r_id=r_id)
            delete_room = rooms.delete_one({'_id': ObjectId(r_id)})
            if delete_room:
                return {'msg': 'success'}
            else:
                return {'err': 'failure'}
        else:
            return {'err': validation[1]}



def check_facility(f_id):  # check if a facility is valid
    facilities = db.facilities
    current_facility = facilities.find_one({'_id': ObjectId(f_id)})
    if current_facility:
        return current_facility
    else:
        return None


def check_building(f_id, b_id):  # check if a building is valid
    buildings = db.buildings
    current_building = buildings.find_one({'_id': ObjectId(b_id), 'facilityID': ObjectId(f_id)})
    if current_building:
        return current_building
    else:
        return None


def check_room(b_id, r_id):
    rooms = db.rooms
    current_room = rooms.find_one({'_id': ObjectId(r_id), 'buildingID': ObjectId(b_id)})
    if current_room:
        return current_room
    else:
        return None


def validate_room(f_id, b_id, r_id=None):
    res =   {
            'mes' : [],
            'er': []
            }
   
    current_facility = check_facility(f_id)
    if current_facility:
        current_building = check_building(f_id, b_id)
        if current_building:
            if r_id is None:
                return [True, current_building]
            else:    
                current_room = check_room(b_id, r_id)
                if current_room:
                    return [True, current_room]
                else:
                    return [False, 'Invalid room ID']
        else:
            return [False, 'Invalid building ID']
    else:
        return [False, 'Invalid faility ID'] 
