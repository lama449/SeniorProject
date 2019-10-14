from flask_restful import Resource
from SeniorProject import database

db = database.conn_DB()

class Room(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
