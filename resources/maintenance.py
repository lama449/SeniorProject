# maintenance.py
# Endpoints for managing maintenance requests
# Monica Mahon, 11/16/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

db = database.conn_DB()

class Maintenance(Resource):
    def get(self, f_id, r_id=None):
        facilities = db.facilities
        rooms = db.rooms
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if r_id:
                current_room = rooms.find_one({'_id': ObjectId(r_id)})
                if current_room:
                    maintenance_reqs = facilities.find(
                        {'_id': ObjectId(f_id), 'maintenance': {'$elemMatch': {'roomID': ObjectId(r_id)}}},
                        {'_id': 0, 'access_code': 0, 'name': 0, 'private': 0, 'address': 0,
                         'phone': 0, 'description': 0, 'presets': 0, 'attributes': 0})
                    current_req = [req for req in maintenance_reqs]
                    if current_req:
                        return jsonify(current_req)
                    else:
                        return 'No maintenance requests for this room.'
                else:
                    return 'Invalid room'
            else:
                return jsonify(facilities.find_one({'_id': ObjectId(f_id)},
                                           {'_id': 0, 'access_code': 0, 'name': 0, 'private': 0, 'address': 0,
                                            'phone': 0, 'description': 0, 'presets': 0, 'attributes': 0}))
        else:
            return 'Invalid facility'
        pass

    def post(self, f_id, r_id):
        data = request.form
        user = session.get('user')
        facilities = db.facilities
        rooms = db.rooms
        buildings = db.buildings
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if r_id:
                current_room = rooms.find_one({'_id': ObjectId(r_id)}, {'number': 1, 'buildingID': 1, '_id': 1})
                if current_room:
                    if not data.get('description'):
                        return 'Missing maintenance request description'
                    if not data.get('date'):
                        return 'Missing date submitted'
                    if not data.get('status'):
                        return 'Missing maintenance request status'
                    current_building = buildings.find_one({'_id': current_room.get('buildingID')})
                    if not current_building: 
                        return 'No building'
                    newReq = facilities.update({'_id': ObjectId(f_id)},
                                               {'$push': {'maintenance':
                                                              {'_id': ObjectId(),
                                                               'buildingName': current_building.get('name'),
                                                               'roomID': current_room.get('_id'),
                                                               'roomNum': current_room.get('number'),
                                                               'description': data.get('description'),
                                                               'userID': user.get('_id'),
                                                               'date': data.get('date'), 
                                                               'status': data.get('status')}}})
                    currentReq = [req for req in newReq]
                    if currentReq:
                        return jsonify(currentReq)
                else:
                    return 'Invalid room'
            else:
                return 'Missing room'
        else:
            return 'Invalid facility'

    def put(self, f_id, m_id, r_id):
        data = request.form
        facilities = db.facilities
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:  # if facility exists
            if m_id:
                if data.get('status'):
                    updated_request = facilities.update_one({'_id': ObjectId(f_id), 'maintenance._id': ObjectId(m_id)},
                                                            {'$set':
                                                                {
                                                                    'maintenance.$.status': data.get('status')
                                                                }
                                                            })
                    #updatedRequest = [req for req in updated_request]
                    #return jsonify(updated_request)
                    return 'Update successful!' #will fix return later 
                else:
                    return 'Missing status update'
            else:
                return 'Invalid maintenance request ID'
        else:
            return 'Invalid facility ID'

    def delete(self, f_id, m_id=None, r_id=None):
        facilities = db.facilities
        rooms = db.rooms
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            if r_id is None:
                facilities.update({'_id': ObjectId(f_id)},
                                  {'$pull': {'maintenance': {'_id': ObjectId(m_id)}}})
                return 'Delete successful'
            elif m_id:
                return 'Invalid maintenance request ID'
            if m_id is None:
                current_room = rooms.find_one({'_id': ObjectId(r_id)})
                if current_room:
                    facilities.update({'_id': ObjectId(f_id)},
                                      {'$pull': {'maintenance': {'roomID': ObjectId(r_id)}}})
                    return 'Delete successful'
                else:
                    return 'Invalid room ID'
        else:
            return 'Invalid facility'
