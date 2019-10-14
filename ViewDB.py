from pymongo import MongoClient
from pprint import pprint

client = MongoClient(port=27017)
db = client.managementdb

cols = db.collection_names()
for c in cols:
    print(c)

facilities = db.facilities
facilityOne = facilities.find_one({'name':'Rowan University'})
pprint(facilityOne)
