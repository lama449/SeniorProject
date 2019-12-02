from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from flask_restful import *
from bson.json_util import loads, dumps
import bcrypt
from SeniorProject.database import conn_DB
from SeniorProject.resources.reservation import Reservation, UserReservations
from SeniorProject.resources.user import User
from SeniorProject.resources.facility import Facility
from SeniorProject.resources.room import Room
from SeniorProject.resources.building import Building
from SeniorProject.resources.maintenance import Maintenance
from SeniorProject.new_json_encoder import New_JSON_Encoder
from SeniorProject.resources.group import Group
from SeniorProject.resources.userGroup import UserGroup
from SeniorProject.user_check import *
from SeniorProject.resources.userFacility import UserFacility

app = Flask(__name__)
api = Api(app)

app.json_encoder = New_JSON_Encoder
db = conn_DB()


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = db.users
    login_user = users.find_one({'email': data.get('email')})  # find user in db

    # response object
    res = {
        'msg': [],
        'err': []
    }

    if login_user:  # if login user exists check hashed pass
        if bcrypt.hashpw(data.get('password').encode('utf-8'), login_user['password']) == login_user['password']:
            session['user'] = {
                '_id': login_user.get('_id'),
                'email': login_user.get('email'),
                'first_name': login_user.get('first_name'),
                'last_name': login_user.get('last_name'),
                'groupID': login_user.get('groupID')
            }
            res['msg'].append('success')
            return jsonify(res)
        else:
            res['err'].append('Invalid username/password combination')
            return jsonify(res)
    else:
        res['err'].append('Invalid username/password combination')
        return jsonify(res)

@app.route('/logout', methods=['GET'])
def logout():
    session['user'] = None
    return redirect(url_for('home'))

@app.route('/register', methods=['GET'])
def register():
    return render_template('Registration.html')


@app.route("/facility/<f_id>", methods=['GET'])
def facility_page(f_id):
    return render_template("Facility.html", f_id=f_id, admin=check_admin(f_id)) #allows us to use f_id in the html template

@app.route('/management', methods=['GET'])
def management_page():
    if check_logged_in():
        return render_template('Management.html', admin=True)
    else:
        return redirect(url_for('home'))

@app.route('/facility/<f_id>/building/<b_id>', methods=['GET'])
def building_page(f_id, b_id):
    return render_template('Buildings.html', f_id=f_id, b_id=b_id, admin=check_admin(f_id))

@app.route('/facility/<f_id>/building/<b_id>/room/<r_id>', methods=['GET'])
def room_update_page(f_id, b_id, r_id):
    # check if user is an admin first. if not, send back to building page?
    if check_admin(f_id):
        return render_template('Room_Update.html', f_id=f_id, b_id=b_id, r_id=r_id)
    else:
        return redirect(url_for('building_page', f_id=f_id, b_id=b_id))


@app.route('/facility/<f_id>/maintenance', methods=['GET'])
def maintenance_page(f_id):
    if check_admin(f_id):
        return render_template('Maintenance.html', f_id=f_id)
    else:
        return redirect(url_for('facility_page', f_id=f_id))

@app.route('/reservations', methods=['GET'])
def reservations():
    if check_logged_in():
        return render_template('Reservations.html')
    else:
        return redirect(url_for('home'))

@app.route('/facility/<f_id>/building/<b_id>/room/<r_id>/reservation/<res_id>', methods=['GET'])
def reservtions_info(f_id, b_id, r_id, res_id):
    if check_logged_in():
        return render_template('Reservation_Info_Page.html', f_id=f_id, b_id=b_id, r_id=r_id, res_id=res_id)
    else:
        return redirect(url_for('home'))

@app.route('/profile', methods=['GET'])
def profile():
    if check_logged_in():
        return render_template('Profile_Page.html')
    else:
        return redirect(url_for('home'))

@app.route('/facility_creation', methods=['GET'])
def facility_creation():
    if check_logged_in():
        return render_template('Facility_Creation_Page.html')
    else:
        return redirect(url_for('home'))

@app.route('/facility/<f_id>/building_creation', methods=['GET'])
def building_creation(f_id):
    # check if user is an admin first. if not, send back to facility page
    if check_admin(f_id):
        return render_template('Building_Creation_Page.html', f_id=f_id)
    else:
        return redirect(url_for('facility_page', f_id=f_id))

@app.route('/facility/<f_id>/building/<b_id>/room_creation', methods=['GET'])
def room_creation(f_id, b_id):
    # check if user is an admin first. if not, send back to building page
    if check_admin(f_id):
        return render_template('Room_Creation_Page.html', f_id=f_id, b_id=b_id)
    else:
        return redirect(url_for('building_page', f_id=f_id, b_id=b_id))

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        if not check_logged_in():
            return render_template('Forgot_Password.html')
        else:
            return redirect(url_for('home'))
    else:
        res = {
                'msg': [],
                'err': []
        }
        users = db.users
        data = request.json
        email = data.get('email')
        answer = data.get('answer')

        if email is None or email == "":
            res['err'].append('No email')
            return jsonify(res)

        if answer is None or answer == "":
            found_user = users.find_one({'email': email})
            if found_user is None:
                res['err'].append('Invalid email')
                return jsonify(res)
            return jsonify({'question': found_user.get('question')})
        else:
            login_user = users.find_one({'email': email})  # find user in db
            if login_user is None:
                res['err'].append('Invalid email')
                return jsonify(res)
            if bcrypt.hashpw(answer.encode('utf-8'), login_user['answer']) == login_user['answer']:
                session['email'] = email
                session['change_password'] = True
                res['msg'].append('success')
                return jsonify(res)
            else:
                res['err'].append('Wrong answer')
                return jsonify(res)

@app.route('/changepassword', methods=['GET'])
def change_password():
    if not check_logged_in():
        return render_template('Change_Password.html')
    else:
        return redirect(url_for('home'))


api.add_resource(Facility, '/api/facilities', '/api/facilities/<f_id>', endpoint='facility')
api.add_resource(Building, '/api/facilities/<f_id>/buildings', '/api/facilities/<f_id>/buildings/<b_id>', endpoint='building')
api.add_resource(Room, '/api/facilities/<f_id>/buildings/<b_id>/rooms', '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>', endpoint='room')
api.add_resource(Reservation, '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>/reservations', '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>/reservations/<reserv_id>', endpoint='reservation')
api.add_resource(User, '/api/users', '/api/users/<u_id>', endpoint='user')
api.add_resource(Maintenance, '/api/facilities/<f_id>/maintenance', '/api/facilities/<f_id>/maintenance/<m_id>', '/api/facilities/<f_id>/maintenance/room/<r_id>', endpoint='maintenance')
api.add_resource(Group, '/api/facilities/<f_id>/groups', '/api/facilities/<f_id>/groups/<g_id>', endpoint='group')
api.add_resource(UserReservations, '/api/user/reservations', endpoint='user reservations')
api.add_resource(UserGroup, '/api/facilities/<f_id>/users/<u_id>/groups/<g_id>', '/api/facilities/<f_id>/users/groups/<g_id>', endpoint='user group')
api.add_resource(UserFacility, '/api/users/facilities', endpoint='user facility')

if __name__ == '__main__':
    app.run()
