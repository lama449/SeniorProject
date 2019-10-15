from flask import Flask, request, render_template, redirect, url_for, session
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database

db = database.conn_DB()

class Room(Resource):
    def get(self, f_id, b_id, r_id): # return a list of rooms for building
        buildings = db.facilities
        rooms = db.rooms
        current_building = buildings.find_one({'_id': b_id, 'facilityID': f_id})
        
        if current_building:  # if building exists
            rooms = rooms.find({'buildingID': current_building.get('_id')})
            return rooms
        else:
            return 'Invalid building'


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
