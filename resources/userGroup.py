# userGroup.py
# Endpoints for managing returning corresponding user/group relationships
# Monica Mahon, 11/26/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

db = database.conn_DB()
class UserGroup(Resource):
    def get(self, f_id, g_id):
        res = {
            'msg': [],
            'err': []
        }
        facilities = db.facilities
        users = db.users
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            groups = current_facility.get('groups')
            group_id = next(g for g in groups if g['_id'] == ObjectId(g_id))['_id']
            if group_id:
                users_in_group = list(users.find({'groupID': ObjectId(g_id)},{'password': 0, 'answer': 0}))
                return jsonify(users_in_group)
            else:
                return jsonify(res['err'].append('Invalid group ID'))
        else:
            return jsonify(res['err'].append('Invalid facility ID'))

    def post(self, f_id, g_id):  # adds group to user entry
        res = {
            'msg': [],
            'err': []
        }
        data = request.json
        users = db.users
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            current_user = users.find_one({'email': data.get('email')})
            if current_user:
                users.update_one({'email': data.get('email')},
                                 {'$push': {'groupID': ObjectId(g_id)}})
                res['msg'].append('User has been added to the group.')
                return jsonify(res)
            else:
                res['err'].append('Invalid user email address')
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
