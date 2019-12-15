from SeniorProject import database
from bson.objectid import ObjectId
from flask import session

db = database.conn_DB()

def check_logged_in():
    return ( session.get('user') is not None )

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

# check if the logged-in user is in one of the specified groups (g_ids is a list)
# returns True if the user is in one of the groups, False otherwise
def check_group(g_ids):
    users = db.users

    if session.get('user') is None:
        print("no logged in user")
        return False

    current_user = users.find_one({'_id': ObjectId(session.get('user').get('_id'))})
    user_groups = [str(g) for g in current_user.get('groupID')]

    g_ids = [str(g) for g in g_ids]

    print("user_groups:")
    print(user_groups)
    print("g_ids:")
    print(g_ids)

    check_group = any(g in user_groups for g in g_ids)
    print("check_group")
    print(check_group)
    return check_group
