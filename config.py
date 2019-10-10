from flask_pymongo import PyMongo

def getDB():
    app.config["MONGO_URI"] = "mongodb://localhost:27017/managementdb"
    mongo = PyMongo(app)
    return mongo