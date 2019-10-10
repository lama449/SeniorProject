from flask_restful import Resource
from app import getDB

db = getDB()


class Reservation(Resource):
    def get(self):  # returns the reservation information
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass