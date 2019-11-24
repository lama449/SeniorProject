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
            logged_in_user = users.find_one({'_id': ObjectId(session.get('user').get('_id'))}, {'password': 0, 'answer': 0})
            return jsonify(logged_in_user)
        else:
            res['err'].append('No user is logged in.')
            return jsonify(res)

    def post(self):  # creating a new user
        data = request.json
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
        question = data.get('question')
        answer = data.get('answer')
        

        if '@' not in email:
            res['err'].append('Invalid email.')
        if not password:
            res['err'].append('No password')
        if password != password_confirm:
            res['err'].append('Passwords do not match.')
        if not f_name:
            res['err'].append('No first name')
        if not l_name:
            res['err'].append('No last name')
        if not question:
            res['err'].append('No security question')
        if not answer:
            res['err'].append('No security question answer')

        if res['err']:
            return jsonify(res)

        # check if email is associated with another user
        existing_email = users.find_one({'email': email})
        if existing_email:
            res['err'].append('That email already exists.')
            return jsonify(res)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_answer = bcrypt.hashpw(answer.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            'password': hashed_password,
            'email': email,
            'first_name': f_name,
            'last_name': l_name,
            'question': question,
            'answer': hashed_answer,
            'groupID': []
        })
        res['msg'].append('success')
        return jsonify(res)


    def put(self):
        data = request.json
        users = db.users
        facilities = db.facilities
        #response object
        res = {
            'msg': [],
            'err': []
        }

        if data.get('email'):
            # check if all the fields are filled out
            email = data.get('email')
            f_name = data.get('first_name')
            l_name = data.get('last_name')

            if '@' not in email:
                res['err'].append('Invalid email.')
            if not f_name:
                res['err'].append('No First Name')
            if not l_name:
                res['err'].append('No Last Name')

            if res['err']:
                return jsonify(res)

            if email == session.get('user').get('email'):
                # email is the same as it was before, so it's good
                pass
            elif users.find_one({'email': email}):
                # email is associated with another user
                res['err'].append('That email already exists.')
                return jsonify(res)
    
            users.update_one({'_id': ObjectId(session.get('user').get('_id'))}, {
                '$set': {
                    'email': email,
                    'first_name': f_name,
                    'last_name': l_name,
                }
            })
            res['msg'].append('success')

            session['user']['email'] = email
            session['user']['first_name'] = f_name
            session['user']['last_name'] = l_name

            return jsonify(res)
        elif data.get('opsw'):
            # check if all the fields are filled out
            old_password = data.get('opsw')
            new_password = data.get('npsw')
            confirm_password = data.get('cpsw')

            if not old_password:
                res['err'].append('No old password')
            if not new_password:
                res['err'].append('No new password')
            if not confirm_password:
                res['err'].append('No password confirmation')
            login_user = users.find_one({'_id': ObjectId(session.get('user').get('_id'))})  # find user in db
            if bcrypt.hashpw(old_password.encode('utf-8'), login_user['password']) != login_user['password']:
                res['err'].append('Old password is wrong')
            if new_password != confirm_password:
                res['err'].append('Passwords do not match')
            if new_password == old_password:
                res['err'].append('New password is the same as old password')

            if res['err']:
                return jsonify(res)

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            users.update_one({'_id': ObjectId(session.get('user').get('_id'))}, {
                '$set': {
                    'password': hashed_password,
                }
            })
            res['msg'].append('success')

            return jsonify(res)
        elif data.get('question'):
            # check if all the fields are filled out
            question = data.get('question')
            old_answer = data.get('oanswer')
            new_answer = data.get('nanswer')

            if not question:
                res['err'].append('No security question')
            if not old_answer:
                res['err'].append('No old security question answer')
            if not new_answer:
                res['err'].append('No new security question answer')
            login_user = users.find_one({'_id': ObjectId(session.get('user').get('_id'))})  # find user in db
            if bcrypt.hashpw(old_answer.encode('utf-8'), login_user['answer']) != login_user['answer']:
                res['err'].append('Old answer is wrong')

            if res['err']:
                return jsonify(res)

            hashed_answer = bcrypt.hashpw(new_answer.encode('utf-8'), bcrypt.gensalt())

            users.update_one({'_id': ObjectId(session.get('user').get('_id'))}, {
                '$set': {
                    'question': question,
                    'answer': hashed_answer,
                }
            })
            res['msg'].append('success')

            session['user']['question'] = question
            return jsonify(res)
        elif session.get('change_password'):
            # check if all the fields are filled out
            new_password = data.get('npsw')
            confirm_password = data.get('cpsw')

            if not new_password:
                res['err'].append('No new password')
            if not confirm_password:
                res['err'].append('No password confirmation')
            if new_password != confirm_password:
                res['err'].append('Passwords do not match')

            if res['err']:
                return jsonify(res)

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            users.update_one({'email': session.get('email')}, {
                '$set': {
                    'password': hashed_password,
                }
            })

            session['email'] = None
            session['change_password'] = None
            res['msg'].append('success')

            return jsonify(res)
        elif data.get('groupID'): 
            users.update_one({'_id': ObjectId(session.get('user').get('_id'))}, {
                '$push': {
                    'groupID': ObjectId(data.get('groupID'))
                }
            })
        else:
            res['err'].append('Invalid arguments')
            return jsonify(res)


    def delete(self):
        # response object
        res = {
            'msg': [],
            'err': []
        }

        users = db.users
        delete_user = users.delete_one({'_id': ObjectId(session.get('user').get('_id'))})
        if delete_user.deleted_count:
            res['msg'].append('success')
            session['user'] = None
        else:
            res['err'].append('Did not find user')
        return jsonify(res)
