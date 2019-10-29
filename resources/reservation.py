from flask_restful import Resource
from SeniorProject import database

db = database.conn_DB()

class Reservation(Resource):
    def get(self):  # returns the reservation information
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
