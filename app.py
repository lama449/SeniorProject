from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from flask_restful import *
from bson.json_util import loads, dumps
import bcrypt
from SeniorProject.database import conn_DB
from SeniorProject.resources.reservation import Reservation
from SeniorProject.resources.user import User
from SeniorProject.resources.facility import Facility
from SeniorProject.resources.room import Room
from SeniorProject.resources.building import Building
from SeniorProject.resources.maintenance import Maintenance
from SeniorProject.new_json_encoder import New_JSON_Encoder

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
            res['err'].append('Invalid username/password combination1')
            return jsonify(res)
    else:
        res['err'].append('Invalid username/password combination2')
        return jsonify(res)

@app.route('/logout', methods=['GET'])
def logout():
    session['user'] = None
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET'])
def forgot_password():
    return render_template('Forgot_Password.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('Registration.html')


@app.route("/facility/<f_id>", methods=['GET'])
def facility_page(f_id):
    return render_template("Facility.html", f_id=f_id) #allows us to use f_id in the html template

@app.route('/management', methods=['GET'])
def management_page():
    return render_template('Management.html')

@app.route('/facility/<f_id>/building/<b_id>', methods=['GET'])
def building_page(f_id, b_id):
    return render_template('Buildings.html', f_id=f_id, b_id=b_id)

@app.route('/facility/<f_id>/building/<b_id>/room/<r_id>', methods=['GET'])
def room_update_page(f_id, b_id, r_id):
    # TODO: check if user is an admin first. if not, send back to building page?
    return render_template('Room_Update.html', f_id=f_id, b_id=b_id, r_id=r_id)


@app.route('/facility/<f_id>/maintenance', methods=['GET'])
def maintenance_page(f_id):
    return render_template('Maintenance.html', f_id=f_id)

@app.route('/reservations', methods=['GET'])
def reservations():
    return render_template('Reservations.html')

@app.route('/reservations/<res_id>', methods=['GET'])
def reservtions_info(res_id):
    return render_template('Reservations_Info.html', res_id=res_id)

@app.route('/profile', methods=['GET'])
def profile():
    return render_template('Profile_Page.html')

@app.route('/facility_creation', methods=['GET'])
def facility_creation():
    return render_template('Facility_Creation_Page.html')

@app.route('/facility/<f_id>/building_creation', methods=['GET'])
def building_creation(f_id):
    # TODO: check if user is an admin first. if not, send back to management page?
    return render_template('Building_Creation_Page.html', f_id=f_id)

@app.route('/facility/<f_id>/building/<b_id>/room_creation', methods=['GET'])
def room_creation(f_id, b_id):
    # TODO: check if user is an admin first. if not, send back to management page?
    return render_template('Room_Creation_Page.html', f_id=f_id, b_id=b_id)



@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template('calendar.html')


api.add_resource(Facility, '/api/facilities', '/api/facilities/<f_id>', endpoint='facility')
api.add_resource(Building, '/api/facilities/<f_id>/buildings', '/api/facilities/<f_id>/buildings/<b_id>', endpoint='building')
api.add_resource(Room, '/api/facilities/<f_id>/buildings/<b_id>/rooms', '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>', endpoint='room')
api.add_resource(Reservation, '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>/reservations', '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>/reservations/<reserv_id>', endpoint='reservation')
api.add_resource(User, '/api/users', '/api/users/<u_id>', endpoint='user')
api.add_resource(Maintenance, '/api/facilities/<f_id>/maintenance', '/api/facilities/<f_id>/maintenance/<m_id>', '/api/facilities/<f_id>/maintenance/<m_id>/room/<r_id>', endpoint='maintenance')

if __name__ == '__main__':
    app.run()
