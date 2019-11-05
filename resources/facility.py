from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
#from bson.json_util import dumps
from SeniorProject import database

db = database.conn_DB()

class Facility(Resource):
    def get(self, f_id):
        facilities = db.facilities
        current_facility = facilities.find_one({'name': f_id})
        if current_facility:
            return jsonify(current_facility)
            #return dumps(current_facility)
        else:
            return 'Invalid facility'

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
