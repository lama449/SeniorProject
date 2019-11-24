from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from datetime import datetime
from bson.objectid import ObjectId
from SeniorProject import database
from SeniorProject.resources.room import validate_room

db = database.conn_DB()

class Reservation(Resource):
    def get(self, f_id, b_id, r_id, reserv_id=None):  # returns the reservation information
        rooms = db.rooms
        
        val = validate_room(f_id, b_id, r_id)
        if val[0]:  # if room exists
            '''current_reservations = rooms.find_one({'_id': ObjectId(r_id), 'reservations': {'$elemMatch': {'_id': Objec
tId(reserv_id)}}}, {'_id':0, 'reservations':1})'''
            current_reservations = rooms.find_one({'_id': ObjectId(r_id)}, {'_id': 0, 'reservations':1})
            if reserv_id:  # return specific reservation
                for x in current_reservations['reservations']:
                    if x['_id'] is ObjectId(reserv_id):
                        return jsonify(x)
                    else:
                        return {'err': 'Invalid reservation ID'} 
            else:  # return all reservations
                return jsonify(current_reservations)                                      
        else:   
            return {'err': val[1]}

    def post(self, f_id, b_id, r_id):
        res =   {
                'msg': [],
                'err': []
                }
    
        data = request.form
        if not data.get('start_time'):
            res['err'].append('Missing start time')
        if not data.get('end_time'):
            res['err'].append('Missing end time')
        if not data.get('userID'):
            res['err'].append('Missing User ID')
        if res['err']:
            return jsonify(res)
        rooms = db.rooms
        val = validate_room(f_id, b_id, r_id)
        if val[0]:
            reserv_id = ObjectId()
            start_time = datetime.fromisoformat(data.get('start_time'))
            end_time = datetime.fromisoformat(data.get('end_time'))
            new_reservation = rooms.update_one({'_id': ObjectId(r_id)},
                                            {'$push': {'reservations': {
                                                '_id': reserv_id,
                                                'start_time': start_time,
                                                'end_time': end_time,
                                                'userID': ObjectId(data.get('userID'))}}})
            return jsonify(reserv_id)
        else:
            return {'err':val[1]}

    def put(self, f_id, b_id, r_id, reserv_id):
        data = request.form
        rooms = db.rooms
        val = validate_room(f_id,b_id,r_id)
        if val[0]:
            start_time = datetime.fromisoformat(data.get('start_time'))
            end_time = datetime.fromisoformat(date.get('end_time'))
            update_reservation = rooms.update_one({'_id': ObjectId(r_id), 'reservations._id': ObjectId(reserv_id)},
                                    {'$set': {'reservations.$.start_time' : start_time,
                                            'reservations.$.end_time' : end_time}})
            return jsonify(ObjectId(r_id))
        else:
            return {'err':val[1]}

    def delete(self, f_id, b_id, r_id, reserv_id):
        rooms = db.rooms
        val = validate_room(f_id, b_id, r_id)
        if val[0]:
            delete_reservation = rooms.update(
                                    {'_id' : ObjectId(r_id)},
                                        {'$pull': {'reservations': {
                                            '_id': ObjectId(reserv_id)}}})
            if delete_reservation:
                return 'success'
            else:
                return {'err': 'failed'}
        else:
            return {'err': val[1]}
