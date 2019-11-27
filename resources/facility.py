from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
from bson.objectid import ObjectId
import bcrypt
import string
import random
from SeniorProject import database
from SeniorProject.resources.building import Building
from SeniorProject.resources.group import Group
from SeniorProject.user_check import *

db = database.conn_DB()

class Facility(Resource):
    def get(self, f_id=None):
        facilities = db.facilities
        res = {
            'msg': [],
            'err': []
        }

        if (f_id):
            # get one facility based on the facility_id
            current_facility = facilities.find_one({'_id': ObjectId(f_id)})
            if current_facility:
                return jsonify(current_facility)
            else:
                res['err'].append('Invalid Facility')
                return jsonify(res)
        else:
            # search for facilities based on a query string (q) and zip code
            # this is for the search on the home page
            q = request.args.get('q')
            zip_code = request.args.get('zip')
            found_facilities = facilities.find({
                '$and': [
                    {
                        '$or': [
                            {'name': {'$regex': q, '$options': 'i'}},
                            {'description': {'$regex': q, '$options': 'i'}},
                            {'address.address_L1': {'$regex': q, '$options': 'i'}},
                            {'address.address_L2': {'$regex': q, '$options': 'i'}},
                            {'attributes': {'$elemMatch': {'$regex': q, '$options': 'i'}}}
                        ]
                    },
                    {'address.zip': zip_code},
                    {'private': False}
                ]
            })
            found_facilities = [facility for facility in found_facilities]
            return jsonify(found_facilities)

    def post(self):
        facilities = db.facilities
        users = db.users
        data = request.json
        res = {
            'msg': [],
            'err': []
        }

        if data.get('access_code'):
            return jsonify(facilities.find_one({'access_code': data.get('access_code')}))
        while data.get('private') == 'true':
            access_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            check_facility = facilities.find_one({'access_code': access_code})
            if check_facility is None:
                break
        if not data.get('name'):
            res['err'].append('Missing Facility Name Field')
        if data.get('private') is None:
            res['err'].append('Missing Facility Private Field')
        if not data.get('address_L1'):
            res['err'].append('Missing Facility Address Line')
        if not data.get('city'):
            res['err'].append('Missing Facility City')
        if not data.get('state'):
            res['err'].append('Missing Facility State')
        if not data.get('zip'):
            res['err'].append('Missing Facility Zip')
        if not data.get('country'):
            res['err'].append('Missing Facility Country')
        if not data.get('phone'):
            res['err'].append('Missing Facility Phone')

        if res['err']:
            return jsonify(res)

        admin_group_id = ObjectId()

        takeID = facilities.insert_one({
        'name': data.get('name'),
        'private': data.get('private') == 'true',
        'access_code': access_code if (data.get('private') == 'true') else '',
        'address': {
            'address_L1': data.get('address_L1'),
            'address_L2': data.get('address_L2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'zip': data.get('zip'),
            'country': data.get('country')
            },
        'phone': data.get('phone'),
        'description': data.get('description'),
        'presets': {},
        'attributes': [],
        'maintenance': [],
        'groups': [{
            '_id': admin_group_id,
            'name': 'admin'
            }]
        })
        users.update_one({'_id': ObjectId(session.get('user').get('_id'))},
                         {'$push': {'groupID': admin_group_id}})
        return jsonify({'_id': takeID.inserted_id})

    def put(self, f_id):
        data = request.json
        facilities = db.facilities
        res = {
            'msg': [],
            'err': []
        }
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if not check_admin(f_id):
            res['err'].append('You do not have the permissions to edit this facility.')
            return jsonify(res)
        if current_facility:
            updated_facility = facilities.update_one({'_id': ObjectId(f_id)},
                {'$set':
                    {'name': data.get('name'),
                     'address': {
                          'address_L1': data.get('address_L1'),
                          'address_L2': data.get('address_L2'),
                          'city': data.get('city'),
                          'state': data.get('state'),
                          'zip': data.get('zip'),
                          'country': data.get('country')},
                      'phone': data.get('phone'),
                      'description': data.get('description')}
                })
            res['msg'].append('success')
            return jsonify(res)
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)

    def delete(self, f_id):
        facilities = db.facilities
        buildings = db.buildings
        rooms = db.rooms
        res = {
            'msg': [],
            'err': []
        }
        current_facility = facilities.find_one({'_id': ObjectId(f_id)})
        if current_facility:
            dbuildings = buildings.find({'facilityID': ObjectId(f_id)})
            for building in dbuildings:
                Building().delete(f_id, str(building.get('_id')))
            dgroups = current_facility.get('groups')
            for group in dgroups:
                Group().delete(f_id, str(group.get('_id')))
            facilities.delete_one({'_id': ObjectId(f_id)})   
            res['msg'].append('success')
        else:
            res['err'].append('Invalid facility')
            return jsonify(res)

