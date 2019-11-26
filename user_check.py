from SeniorProject import database
from bson.objectid import ObjectId
from flask import session

db = database.conn_DB()

def check_logged_in():
    pass

def check_admin(f_id):
    facilities = db.facilities
    users = db.users

    current_facility = facilities.find_one({'_id': ObjectId(f_id)})
    if current_facility is None:
        return False

    groups = current_facility.get('groups')

    # find the admin group and get its id
    # see https://stackoverflow.com/a/8653568
    admin_id = next(g for g in groups if g['name'] == 'admin')['_id']

    if session.get('user') is None:
        return False

    admin_user = users.find_one({'_id': ObjectId(session.get('user').get('_id')), 'groupID': ObjectId(admin_id)})
    if admin_user is None:
        return False
    else:
        return True
