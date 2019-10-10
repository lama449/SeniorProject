from pymongo import MongoClient


def conn_DB():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.managementdb
    return db


'''def getDB(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/managementdb"
    mongo = PyMongo(app)
    return mongo'''