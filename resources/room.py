from flask import Flask, request, render_template, redirect, url_for, session
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database

db = database.conn_DB()

class Room(Resource):
    def get(self, f_id, b_id, r_id=None): # return a list of rooms for building
        rooms = db.rooms
        if r_id is None:
            return {'message': 'room list'}
        facilities = db.facilities
        buildings = db.buildings
        current_facility = facilities.find_one({'name': f_id})
        if current_facility:
            current_building = buildings.find_one({'name': b_id, 'facilityID': current_facility.get('_id')})
                                               
            if current_building:  # if building exists
                current_rooms = rooms.find({'buildingID': current_building.get('_id')})
                return dumps(current_rooms)
            else:
                return 'Invalid building'
        else:
            return 'Invalid facility'


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
