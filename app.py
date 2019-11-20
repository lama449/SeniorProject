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
    print(data.get('email'))
    print(login_user)

    # response object
    res = {
        'msg': [],
        'err': []
    }

    if login_user:  # if login user exists check hashed pass
        if bcrypt.hashpw(data.get('password').encode('utf-8'), login_user['password']) == login_user['password']:
            session['user'] = {
                '_id': login_user.get('_id')
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

@app.route('/facility', methods=['GET'])
def reservations():
    return render_template('Facility.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('Registration.html')

@app.route('/schedule', methods=['GET'])
def schedule():
    return render_template('Schedule.html')

@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template('calendar.html')

@app.route('/building_creation', methods=['GET'])
def building_creation():
    return render_template('Building_Creation_Page.html')

api.add_resource(Facility, '/api/facilities', '/api/facilities/<f_id>', endpoint='facility')
api.add_resource(Building, '/api/facilities/<f_id>/buildings', '/api/facilities/<f_id>/buildings/<b_id>', endpoint='building')
api.add_resource(Room, '/api/facilities/<f_id>/buildings/<b_id>/rooms', '/api/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>', endpoint='room')
api.add_resource(Reservation, '/api/reservations', endpoint='reservation')
api.add_resource(User, '/api/users', '/api/users/<u_id>', endpoint='user')
api.add_resource(Maintenance, '/api/facilities/<f_id>/maintenance', '/api/facilities/<f_id>/maintenance/<r_id>', endpoint='maintenance')

if __name__ == '__main__':
    app.run(debug=True)
