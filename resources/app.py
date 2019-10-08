from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import *
from resources.reservation import Reservation

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/managementdb"
mongo = PyMongo(app)


@app.route('/login', methods = ['POST'])
def login():
    # login


@app.route('/register', methods = ['POST'])
def register():
    # register


api.add_resource(Reservation, '/reservations', '/reservations:<str:id>')
