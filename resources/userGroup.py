# userGroup.py
# Endpoints for managing maintenance requests
# Monica Mahon, 11/26/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

db = database.conn_DB()
class UserGroup(Resource):
    def get(self):
        pass

    def post(self, f_id, u_id, g_id):  # adds group to user entry
        res = {
            'msg': [],
            'err': []
        }
        users = db.users
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            current_user = users.find_one({'_id': ObjectId(u_id)})
            if current_user:
                users.update_one({'_id': ObjectId(u_id)},
                                 {'$push': {'groupID': ObjectId(g_id)}})
                res['msg'].append('User has been added to the group.')
                return jsonify(res)
            else:
                res['err'].append('Invalid user ID')
                return jsonify(res)
        else:
            res['err'].append('Invalid facility ID')
            return jsonify(res)

    def put(self, u_id, g_id):
        pass

    def delete(self, f_id, u_id, g_id):  # just deletes group from user entry
        res = {
            'msg': [],
            'err': []
        }
        users = db.users
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            current_user = users.find_one({'_id': ObjectId(u_id)})
            if current_user:
                users.update_one({'_id': ObjectId(u_id)},
                                 {'$pull': {'groupID': ObjectId(g_id)}})
                res['msg'].append('User has been removed from the group.')
                return jsonify(res)
            else:
                res['err'].append('Invalid user ID')
                return jsonify(res)
        else:
            res['err'].append('Invalid facility ID')
            return jsonify(res)
