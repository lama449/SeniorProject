from flask import Flask, request, render_template, redirect, url_for, session
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database

db = database.conn_DB()

class User(Resource):

    def get(self):
        users = db.users
        print(users)

    def post(self):  # creating a new user
        # load template, then pass info to User resource to POST new user
        # session['username'] = request.json['username']  # session retruned user
        data = request.form
        users = db.users
        existing_user = users.find_one({'username': data.get('username')})
        if existing_user is None:
            email = data.get('email')
            existing_email = users.find_one({'email': email})
            if '@' not in email or existing_email:
                return 'That email already exists.'
    
            hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
            users.insert({
                'username': data.get('username'),
                'password': hashed_password,
                'email': email,
                'first_name': '',
                'last_name': '',
                'groupID': []
            })
            session['username'] = data.get('username')
            return redirect(url_for('calendar'))
        else:
            return 'That username already exists.'


    def put(self):
        pass

    def delete(self):
        pass
