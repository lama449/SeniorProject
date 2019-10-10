from flask_restful import Resource, request
import bcrypt
from app import getDB

mongo = getDB()


class User(Resource):
    def get(self):
        users = mongo.db.users
        print(users)

    def post(self):  # creating a new user
        data = request.json

        users = mongo.db.users
        existing_user = users.find_one({'username': data.get('username')})  # try to find username in the db

        if existing_user is None:  # create user
            hashpass = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': data.get('username'), 'password': hashpass})
            return {'username': data.get('username')}
        else:
            return {'message': 'username already exists'}

    def put(self):
        pass

    def delete(self):
        pass