# userMaintenance.py
# Endpoints for managing maintenance requests
# Monica Mahon, 12/10/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

db = database.conn_DB()


class UserMaintenance(Resource):
#    def get(self, u_id):
#        res = {
#            'msg': [],
#            'err': []
#        }
#        users = db.users
#        facilities = db.facilities
#        if u_id:
#            current_user = users.find_one({'_id': ObjectId(u_id)})
#            if current_user:
#                maintenance_requests = list(
#                    facilities.find({'maintenance': {'$elemMatch': {'userID': {ObjectId(u_id)}}}}))
#                if maintenance_requests:
#                    return jsonify(maintenance_requests)
#                else:
#                    return jsonify(res['msg'].append('User does not have any maintenance requests.'))
#            else:
#               return jsonify(res['err'].append('Invalid user ID'))

    def get(self):
        res = {
            'msg': [],
            'err': []
        }
        users = db.users
        facilities = db.facilities
        u_id = session.get('user').get('_id')
        if u_id:
            current_user = users.find_one({'_id': ObjectId(u_id)})
            if current_user:
                # ////
                maintenance_requests = facilities.aggregate([
                    {
                        "$match": {
                            "maintenance": {
                                "$elemMatch": {'userID': ObjectId(u_id)}
                            }
                        }
                    },
                    {
                        "$unwind": "$maintenance"
                    },
                    {
                        "$match": {
                            "maintenance.userID": ObjectId(u_id)
                        }
                    },
                    {
                        "$project": {"maintenance": 1, "name": 1}
                    }
                ])

                # /////
                #maintenance_requests = list(
                #    facilities.find({'maintenance': {'$elemMatch': {'userID': ObjectId(u_id)}}}, {'name': 1, 'maintenance':1}))
                maintenance_requests = [r for r in maintenance_requests]
                if maintenance_requests:
                    return jsonify(maintenance_requests)
                else:
                    res['msg'].append('User does not have any maintenance requests.')
                    return jsonify(res)
            else:
                res['err'].append('Invalid user ID')
                return jsonify(res)
        else: 
            res['err'].append('missing u_id')
            return jsonify(res)

def post(self, f_id, r_id):
    pass


def put(self, f_id, m_id):
    pass


def put(self):
    pass


def delete(self, f_id, m_id, r_id=None):
    pass
