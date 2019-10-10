from flask import Flask, redirect, request, session, url_for
from flask_pymongo import PyMongo
from flask_restful import *
import bcrypt

app = Flask(__name__)
api = Api(app)

def getDB():
    app.config["MONGO_URI"] = "mongodb://localhost:27017/managementdb"
    mongo = PyMongo(app)
    return mongo

mongo = getDB()


@app.route('/')
@app.route('/home')
def home():
    return 'This is a page. I made this :)'


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = mongo.db.users
    login_user = users.find_one({'username': data.get('username')})  # find user in db

    if login_user:  # if login user exists check hashed pass
        if bcrypt.hashpw(data.get('password').encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = data.get('username')
            return redirect(url_for('home'))

        else:
            return 'Invalid username/password combination'


@app.route('/register', methods=['GET'])
def register():
    print('load register page then POST to user resource with data to create')
    session['username'] = request.form['username']  # session retruned user


from resources.reservation import Reservation
from resources.user import User

api.add_resource(Reservation, '/reservations', '/reservations/<id>')
api.add_resource(User, '/users', '/users/<id>')

if __name__ == '__main__':
    app.run(debug=True)
