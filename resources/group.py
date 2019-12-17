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
        res = {
            'msg': [],
            'err': []
        }
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
                    res['err'].append('No groups to display')
                    return jsonify(res)
        else: 
            res['err'].append('Invalid facility ID')
            return jsonify(res)


    def post(self, f_id):
        data = request.json
        facilities = db.facilities
        res = {
            'msg': [],
            'err': []
        }
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if not data.get('name'):
                res['err'].append('Missing group name')
                return jsonify(res)
            else:
                facilities.update({'_id': ObjectId(f_id)},
                                              {'$push': {'groups': {'_id': ObjectId(),
                                                                   'name': data.get('name')}}})
                res['msg'].append('success')
                return jsonify(res)
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)

    def put(self, f_id, g_id):
        data = request.form
        facilities = db.facilities
        res = {
            'msg': [],
            'err': []
        }
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
                    res['msg'].append('Updated the group name')
                    return jsonify(res)
                else:
                    res['err'].append('Missing new name')
                    return jsonify(res)
            else:
                res['err'].append('Missing group ID')
                return jsonify(res)
        else:
            res['err'].append('Invalid facility ID')
            return jsonify(res)


    def delete(self, f_id, g_id):
        facilities = db.facilities
        users = db.users
        res = {
            'msg': [],
            'err': []
        }
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            groups = current_facility.get('groups')
            admin_id = next(g for g in groups if g['name'] == 'admin')['_id']
            default_id = next(d for d in groups if d['name'] == 'default')['_id']
            if (ObjectId(g_id) != admin_id) and (ObjectId(g_id) != default_id):
                facilities.update({'_id': ObjectId(f_id)},
                                  {'$pull': {'groups': {'_id': ObjectId(g_id)}}})
                users.update({'groupID': ObjectId(g_id)},
                             {'$pull': {'groupID': ObjectId(g_id)}})
                res['msg'].append('Delete successful')
                return jsonify(res)
            else:
                res['msg'].append('Cannot delete admin or default group.')
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)

    def obliterate(self, f_id, g_id):
        facilities = db.facilities
        users = db.users
        res = {
            'msg': [],
            'err': []
        }
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            group = facilities.find_one({'groups': {'_id': ObjectId(g_id)}, 'groups.name': 1})
            facilities.update({'_id': ObjectId(f_id)},
                                  {'$pull': {'groups': {'_id': ObjectId(g_id)}}})
            users.update({'groupID': ObjectId(g_id)},
                             {'$pull': {'groupID': ObjectId(g_id)}})
            res['msg'].append('Delete successful')
            return jsonify(res)
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)



#    def delete(self, f_id, g_id):
#        facilities = db.facilities
#        users = db.users
#        res = {
#            'msg': [],
#            'err': []
#        }
#        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
#        if current_facility:
#            facilities.update({'_id': ObjectId(f_id)},
#                              {'$pull': {'groups': {'_id': ObjectId(g_id)}}})
#            users.update({'groupID': ObjectId(g_id)},
#                         {'$pull': {'groupID':  ObjectId(g_id)}})
#            res['msg'].append('Delete successful')
#            return jsonify(res)
#        else:
#            res['err'].append('Invalid facility')
#            return jsonify(res)
