from flask import Flask
from flask_restful import Api
from resources.facility import *
from resources.building import *
from resources.room import *
from resources.reservation import *
from resources.maintenance import *
from resources.user import *
from resources.group import *

app = Flask(__name__)
api = Api(app)

