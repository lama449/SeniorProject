# userFacility.py
# Endpoints for viewing which facilities a user is an admin of. 
# Monica Mahon, 11/26/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

db = database.conn_DB()


class UserFacility(Resource):
    def get(self):
        res = {
            'msg': [],
            'err': [],
            'facilities': []
        }
        facilities = db.facilities
        users = db.users
        current_user = users.find_one({'_id': ObjectId(session.get('user').get('_id'))})
        #current_user = users.find_one({'_id': ObjectId(u_id)})
        current_facilities = facilities.find({})
        userGroups = current_user.get('groupID')
        if current_user:
            for current_facility in current_facilities:
                groups = current_facility.get('groups')
                admin_id = next(g for g in groups if g['name'] == 'admin')['_id']
                for userGroup in userGroups:
                    if admin_id == userGroup:
                        res['facilities'].append(current_facility)
        else:
            res['err'].append('Invalid user')
            return jsonify(res)
        if not res['facilities']:
            res['msg'].append('User is not an admin for any facilities')
            return jsonify(res)
        else:
            return jsonify(res)
        
    def post(self):
        pass


    def put(self):
        pass


    def delete(self):
        pass
