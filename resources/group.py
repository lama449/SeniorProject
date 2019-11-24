# groups.py
# Endpoints for managing maintenance requests
# Monica Mahon, 11/23/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

db = database.conn_DB()

class Group(Resource):
    def get(self, f_id, g_id=None):
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if g_id is None:
                return jsonify(facilities.find_one({'_id': ObjectId(f_id)},
                                                   {'_id': 0, 'access_code': 0, 'name': 0, 'private': 0, 'address': 0,
                                                    'phone': 0, 'description': 0, 'presets': 0, 'attributes': 0,
                                                    'maintenance': 0}))
            else:
                groups = facilities.find(
                    {'_id': ObjectId(f_id), 'groups': {'$elemMatch': {'_id': ObjectId(g_id)}}},
                    {'_id': 0, 'access_code': 0, 'name': 0, 'private': 0, 'address': 0,
                     'phone': 0, 'description': 0, 'presets': 0, 'attributes': 0, 'maintenance': 0})
                current_group = [group for group in groups]
                if current_group:
                    return jsonify(current_group)
                else: 
                    return 'No groups to display'
        else: 
            return 'Invalid facility ID'


    def post(self, f_id):
        data = request.json
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if not data.get('name'):
                return 'Missing group name'
            else:
                facilities.update({'_id': ObjectId(f_id)},
                                              {'$push': {'groups': {'_id': ObjectId(),
                                                                   'name': data.get('name')}}})
                return 'Added group'
        else:
            return 'Invalid facility'

    def put(self, f_id, g_id):
        data = request.form
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if g_id:
                if data.get('name'):
                    facilities.update_one({'_id': ObjectId(f_id), 'groups._id': ObjectId(g_id)},
                                                            {'$set':
                                                                {
                                                                    'groups.$.name': data.get('name')
                                                                }
                                                            })
                    return 'Updated the group name' 
                else:
                    return 'Missing new name'
            else:
                return 'Missing group ID'
        else:
            return 'Invalid facility ID'

    def delete(self, f_id, g_id):
        facilities = db.facilities
        users = db.users
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            facilities.update({'_id': ObjectId(f_id)},
                              {'$pull': {'groups': {'_id': ObjectId(g_id)}}})
            users.update({'groupID': ObjectId(g_id)},
                         {'$pull': {'groupID':  ObjectId(g_id)}})
            return 'Delete successful'
        else:
            return 'Invalid facility'
