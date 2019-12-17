from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from datetime import datetime, timedelta
from dateutil import parser
from bson.objectid import ObjectId
from SeniorProject import database
from SeniorProject.resources.room import validate_room
from SeniorProject.user_check import *

db = database.conn_DB()

class Reservation(Resource):
    def get(self, f_id, b_id, r_id, reserv_id=None):  # returns the reservation information
        res =   {
                'msg': [],
                'err': []
                }
        rooms = db.rooms
        
        val = validate_room(f_id, b_id, r_id)
        if val[0]:  # if room exists
            current_reservations = rooms.find_one({'_id': ObjectId(r_id)}, {'_id': 0, 'reservations':1})
            if reserv_id:  # return specific reservation
                for x in current_reservations['reservations']:
                    if ObjectId(x['_id']) == ObjectId(reserv_id):
                        return jsonify(x)
                res['err'].append('Invalid reservation ID')
                return res
            else:  # return all reservations
                return jsonify(current_reservations)                                      
        else:   
            res['err'].append(val[1])

    def post(self, f_id, b_id, r_id):
        res =   {
                'msg': [],
                'err': []
                }
        rooms = db.rooms
        
        #groups = rooms.aggregate([
                        #{
                            #'$match': {
                                #'_id': ObjectId(r_id)
                        #}
                        #},
                        #{
                            #'$project': {'_id': 1, 'groupID': 1}
                        #},
                        #{
                            #'$unwind': '$groupID'
                        #}])

        room_groups = rooms.find_one({'_id': ObjectId(r_id)}).get('groupID')

        if not check_group(room_groups):
            res['err'].append('You do not have the permissions to create a reservation.')
            return jsonify(res)

        data = request.json
        if not data.get('start_time'):
            res['err'].append('Missing start time')
        if not data.get('end_time'):
            res['err'].append('Missing end time')
        # if not data.get('userID'):
            # res['err'].append('Missing User ID')
        if res['err']:
            return jsonify(res)

        userID = session.get('user').get('_id')
        rooms = db.rooms
        val = validate_room(f_id, b_id, r_id)
        if val[0]:
            reserv_id = ObjectId()
            start_time = parser.parse(data.get('start_time'))
            end_time = parser.parse(data.get('end_time'))
            time_val = validate_timeslot(start_time, end_time, r_id)
            curr_time = validate_time(start_time)
            print(time_val)
            if curr_time[0]:
                if time_val[0]:    
                    new_reservation = rooms.update_one({'_id': ObjectId(r_id)},
                                                    {'$push': {'reservations': {
                                                        '_id': reserv_id,
                                                        'start_time': start_time,
                                                        'end_time': end_time,
                                                        'userID': ObjectId(userID)}}})
                    return jsonify({'_id': reserv_id})
                else:
                    res['err'].append(time_val[1]['err'])
                    return res
            else:
                res['err'].append(curr_time[1]['err'])
                return res
        else:
            res['err'].append(val[1])
            return jsonify(res)

    '''
    def put(self, f_id, b_id, r_id, reserv_id):
        data = request.json
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
    '''
    
    def delete(self, f_id, b_id, r_id, reserv_id):
        res = {
            'msg': [],
            'err': []
        }

        rooms = db.rooms
        val = validate_room(f_id, b_id, r_id)
        if val[0]:
            u_id = session.get('user').get('_id')
            room_reservations = rooms.aggregate([
                        {
                            '$match': {
                                '_id': ObjectId(r_id)
                        }
                        },
                        {
                            '$project': {'_id': 1, 'reservations': 1}
                        },
                        {
                            '$unwind': '$reservations'
                        },
                        {
                            '$match': {
                                'reservations._id': ObjectId(reserv_id),
                                'reservations.userID': ObjectId(u_id)
                        }}
            ])
            match = [r for r in room_reservations]
            if not (check_admin(f_id) or len(match)!= 0):
                res['err'].append('You do not have the permissions to delete this reservation.')
                return jsonify(res)

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


class UserReservations(Resource):
    def get(self):
        rooms = db.rooms
        users = db.users
        # u_id = session.get(user.get('_id'))
        data = request.form
        #u_id = data.get('userID')
        u_id = session.get('user').get('_id')
        #rooms = rooms.find( {'reservations':
                            #{'$elemMatch': {'userID': ObjectId(u_id)}}},
                            #{'reservations':1})




        reservations = rooms.aggregate([
            {
                "$match": {
                    "reservations": {
                        "$elemMatch": {'userID': ObjectId(u_id)}
                    }
                }
            },
            {
                "$unwind": "$reservations"
            },
            {
                "$match": {
                    "reservations.userID": ObjectId(u_id)
                }
            },
            {
                "$lookup": {
                    "from": "buildings",
                    "localField": "buildingID",
                    "foreignField": "_id",
                    "as": "building"
                }
            },
            {
                "$unwind": "$building"
            },
            {
                "$lookup": {
                    "from": "facilities",
                    "localField": "building.facilityID",
                    "foreignField": "_id",
                    "as": "facility"
                }
            },
            {
                "$unwind": "$facility"
            },
            {
                "$project": {"reservations": 1, "facility._id": 1, "facility.name": 1, "building._id": 1, "building.name": 1, "name": 1, "number": 1}
            }
        ])


        reservations = [ r for r in reservations ]
        return jsonify(reservations)

# validate the time specified
def validate_time(start):
    current_time = datetime.utcnow()-timedelta(hours=5)
    print(start, current_time, (current_time-timedelta(hours=5)))
    if current_time > start:
        return [False, {'err': 'Cannot make a reservation for past timeslot'}]
    else:
        return [True, {'success'}]
   

def validate_timeslot(start, end, r_id):
    rooms = db.rooms
    u_id = session.get('user').get('_id')

    # validate rooms timeslots
    room_reservations = rooms.aggregate([
        {
            '$match': {
                 '_id': ObjectId(r_id)
            }
        },
        {
            '$project': {'_id': 1, 'reservations': 1}
        },
        {
            '$unwind': '$reservations'
        },
        {
            '$match': {
                '_id': ObjectId(r_id),
                '$or':[
                    {'$and':[   {'reservations.start_time': {'$gte': start}},
                                {'reservations.end_time':   {'$lte': end}}
                            ]},
                    {'$and':[   {'reservations.start_time': {'$lte': start}},
                                {'reservations.end_time':   {'$gte': end}}
                            ]},
                    {'$and':[   {'reservations.start_time': {'$lte': start}},
                                {'reservations.end_time':   {'$gt': start, '$lt': end}}
                            ]},
                    {'$and':[   {'reservations.start_time': {'$gt': start, '$lt': end}},
                                {'reservations.end_time':   {'$gte': end}}
                            ]}
                    ]
            }
        }
    ])

    room_conflicts = [ r for r in room_reservations]
    if len(room_conflicts) != 0:
        return [False,{'err': 'Reservation for current room overlaps'}]

    # validate users timeslot
    user_reservations = rooms.aggregate([
        {
            '$match':   {
                'reservations': {
                    '$elemMatch': { 'userID': ObjectId(u_id)}
                                }}
        },                         
        {
            '$project': {'_id': 0, 'reservations': 1}
        },
        {
            '$unwind': '$reservations'
        },
        {
            '$match': {
                'reservations.userID': ObjectId(u_id),
                '$or':[
                    {'$and':[   {'reservations.start_time': {'$gte': start}},
                                {'reservations.end_time':   {'$lte': end}}
                            ]},
                    {'$and':[   {'reservations.start_time': {'$lte': start}},
                                {'reservations.end_time':   {'$gte': end}}
                            ]},
                    {'$and':[   {'reservations.start_time': {'$lte': start}},
                                {'reservations.end_time':   {'$gt': start, '$lt': end}}
                            ]},
                    {'$and':[   {'reservations.start_time': {'$gt': start, '$lt': end}},
                                {'reservations.end_time':   {'$gte': end}}
                            ]}
                    ]
            }
        }
    ])

    user_conflicts = [ r for r in user_reservations ]
    if len(user_conflicts) == 0:
        return [True, {'msg': 'success'}]
    else:
        return [False, {'err': 'User has a current reservation that overlaps'}]


