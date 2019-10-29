####################################################################################
# Monica Mahon
# Prototype
#
# Reservation Creator
# Checks validates if the room exists, then pushes the reservation to the database if
# the user entered time is free
#
####################################################################################

from pymongo import MongoClient
import sys

client = MongoClient(port=27017)
db = client.managementdb

facilities = db.facilities
buildings = db.buildings
rooms = db.rooms

facilityName = input("Enter the name of the facility you'd like to make a reservation in: ")
facility = facilities.find_one({"name": facilityName})

if facility is None:
    print("Facility does not exist")
    sys.exit()

buildingName = input("Enter the name of the building you'd like to make a reservation in:")

building = buildings.find_one({"$and": [ {"name": buildingName}, {"facilityID": facility.get("_id")} ] })

if building is None:
    print("Building does not exist")
    sys.exit()

print(building.get("_id"))
roomNumber = input("Enter your room number: ")

ifRoom = rooms.find_one({"$and": [{"number":int (roomNumber)}, {"buildingID": building.get("_id") }]})

if ifRoom is None:
    print("Room does not exist.")
    sys.exit()
else:
    time = input("Enter a time for your reservation: ")
    cursor = rooms.find_one({"$and": [{"reservations.start_time": time}, {"number":int (roomNumber)}]})
    if cursor is None:
        rooms.update_one(
            {"number": int (roomNumber)},
            {"$push": {
                "reservations": {
                    "start_time": time,
                    "end_time": "",
                     "userID": ""
                }
            }
            }
        )
        print("Reservation accepted for " + time)
    else:
        print("Reservation time is occupied.")
        sys.exit()

