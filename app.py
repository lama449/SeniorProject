from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import *
import bcrypt

app = Flask(__name__)
api = Api(app)

def getDB():
    app.config["MONGO_URI"] = "mongodb://localhost:27017/managementdb"
    mongo = PyMongo(app)
    return mongo

@app.route('/', '/home')
def home():
    return 'This is a page. I made this :)'

@app.route('/login', methods = ['POST'])
def login():
    # login

from resources.reservation import Reservation
api.add_resource(Reservation, '/reservations', '/reservations/<str:id>')
