from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
from bson.objectid import ObjectId
import bcrypt
from SeniorProject import database

db = database.conn_DB()

class User(Resource):

    def get(self):
        users = db.users
        # response object
        res = {
            'msg': [],
            'err': []
        }

        if session.get('user'):
            logged_in_user = users.find_one({'_id': ObjectId(session.get('user').get('_id'))}, {'password': 0})
            return jsonify(logged_in_user)
        else:
            res['err'].append('No user is logged in.')
            return jsonify(res)

    def post(self):  # creating a new user
        # load template, then pass info to User resource to POST new user
        # session['username'] = request.json['username']  # session retruned user
        data = request.form
        users = db.users
        #response object
        res = {
            'msg': [],
            'err': []
        }

        # check if all the fields are filled out
        email = data.get('email')
        password = data.get('password1')
        password_confirm = data.get('password2')
        f_name = data.get('fname')
        l_name = data.get('lname')

        if '@' not in email:
            res['err'].append('Invalid email.')
        if not password:
            res['err'].append('No password')
        if password != password_confirm:
            res['err'].append('Passwords do not match.')
        if not f_name:
            res['err'].append('No First Name')
        if not l_name:
            res['err'].append('No Last Name')

        if res['err']:
            return jsonify(res)

        # check if email is associated with another user
        existing_email = users.find_one({'email': email})
        if existing_email:
            res['err'].append('That email already exists.')
            return jsonify(res)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert({
            'password': hashed_password,
            'email': email,
            'first_name': f_name,
            'last_name': l_name,
            'groupID': []
        })
        res['msg'].append('success')
        return jsonify(res)


    def put(self):
        pass

    def delete(self):
        pass
