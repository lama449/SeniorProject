from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from bson.objectid import ObjectId
#from bson.json_util import dumps
from SeniorProject import database

db = database.conn_DB()

class Room(Resource):
    def get(self, f_id, b_id, r_id=None): # return a list of rooms for building
        rooms = db.rooms
        facilities = db.facilities
        buildings = db.buildings
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            current_building = buildings.find_one({'_id': ObjectId(b_id), 'facilityID': current_facility.get('_id')})
                                               
            if current_building:  # if building exists
                if r_id is None:  # return list of rooms
                    current_rooms = rooms.find({'buildingID': current_building.get('_id')})

                    # convert the Cursor object to a dictionary so that it is JSON serializable
                    current_rooms = [room for room in current_rooms]
                    return jsonify(current_rooms)
                    #return dumps(current_rooms)
                else:  # specific room
                    current_room = rooms.find_one({'_id': ObjectId(r_id), 'buildingID': current_building.get('_id')})
                    if current_room:
                        return jsonify(current_room)
                        #return dumps(current_room)
                    else:
                        return 'Invalid room'
            else:
                return 'Invalid building'
        else:
            return 'Invalid facility'


    def post(self, f_id, b_id):
        data = request.form
        if not data.get('name'):
            return 'Missing room name'
        if not data.get('capacity'):
            return 'Missing room capacity'
        if not data.get('number'):
            return 'Missing room number'
        
        rooms = db.rooms
        facilities = db.facilities
        buildings = db.buildings
        
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            current_building = buildings.find_one({'_id': ObjectId(b_id), 'facilityID': current_facility.get('_id')})                                 
            if current_building:  # if building exists
                takeID = rooms.insert_one({
                'attributes': {},
                'buildingID' : current_building.get('_id'),
                'capacity': data.get('capacity'),
                'groupID': {},
                'name': data.get('name'),
                'number': data.get('number'),
                'reservations': {}
                })
                return jsonify(takeID.inserted_id)
            else:
                return 'Invalid building'
        else:
            return 'Invalid facility'

    def put(self):
        pass

    def delete(self):
        pass
