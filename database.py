from pymongo import MongoClient


def conn_DB():
    client = MongoClient('mongodb://localhost:27017/')
    # client = MongoClient("mongodb://ec2-35-170-202-37.compute-1.amazonaws.com/managementdb")
    # client = MongoClient('mongodb://test:BigF@172.31.83.61/managementdb')
    db = client.managementdb
    return db


'''def getDB(app):
    app.config["MONGO_URI"] = "mongodb://ec2-35-170-202-37.compute-1.amazonaws.com/managementdb"
    mongo = PyMongo(app)
    return mongo'''