from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from resources.facility import *
from resources.building import *
from resources.room import *
from resources.reservation import *
from resources.maintenance import *
from resources.user import *
from resources.group import *

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/managementdb"
mongo = PyMongo(app)


@app.route('/login', methods = ['POST'])
def login():
    # login

api.add_resource(Reservation, '/reservations', '/reservations/<str:id>')
