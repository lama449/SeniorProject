'''
Alex Lam
Facility prototype for creating facilities.
This is a prototype to push a facility into the database.
10/12/19

NOTES: Input fields will be replaced with text fields from the website to run this code.
'''
from pymongo import MongoClient
from pprint import pprint

client = MongoClient(port=27017)
db = client.managementdb
facilities = db.facilities

print("Welcome to the facility creator for our Senior Project!")
print()
facTitle = input("Enter the facility name: ")
print("The facility's name is: " + facTitle)
addressLine1 = input("Enter the address Line 1: ")
print("Address Line 1: " + addressLine1)
addressLine2 = input("Enter the address Line 2: ")
print("Address Line 2: " + addressLine2)
city = input("Enter the city: ")
print("City: " + city)
state = input("Enter the state: ")
print("State: " + state)
zipCode = input("Enter the Zip: ")
print("Zip: " + str(zipCode))
country = input("Enter the country: ")
print("Country: " + str(country))
print()

# Access code
accessCode = input("Enter Access Code: ")
print("Access code: " + str(accessCode))

# Phone
phone = input("Enter the phone number: ")
print("Phone: " + str(phone))

# Description
desc = input("Enter a description: ")
print("The description is: " + str(desc))

mydict = {"name": facTitle, "address": {"address_L1": addressLine1, "address_L2": addressLine2,
                                         "city": city, "state": state, "zipCode": zipCode, "country": country},
          "access_code": accessCode, "private": False, "phone": phone, "description": desc,
          "presets": [], "attributes:": [], "maintenance": []}

x = facilities.insert_one(mydict)
pprint(x)
