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
        current_facility = facilities.find_one({'name': f_id})
        if current_facility:  # if facility exists
            if b_id is None:  # return list of rooms
                current_building = buildings.find({'facilityID': current_facility.get('_id')})
                # convert the Cursor object to a dictionary so that it is JSON serializable
                current_buildings = [building for building in current_building]
                return jsonify(current_buildings)
            else:  # specific building
                current_building = buildings.find_one({'facilityID': current_facility.get('_id'), 'name': b_id })
                if current_building:
                    return jsonify(current_building)
                    # return dumps(current_room)
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
