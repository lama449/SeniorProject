from flask import Flask, redirect, request, session, url_for, render_template
from flask_restful import *
from bson.json_util import loads, dumps
import bcrypt
from SeniorProject.database import conn_DB
from SeniorProject.resources.reservation import Reservation
from SeniorProject.resources.user import User
from SeniorProject.resources.room import Room

app = Flask(__name__)
api = Api(app)

db = conn_DB()


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Login_Page.html')
    else:
        data = request.form
        users = db.users
        login_user = users.find_one({'username': data.get('username')})  # find user in db

        if login_user:  # if login user exists check hashed pass
            if bcrypt.hashpw(data.get('password').encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = data.get('username')
                return redirect(url_for('home'))

        else:
            return 'Invalid username/password combination'


@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template('Schedule.html')
    
@app.route('/scheduling_confirmation', methods=['GET'])
def scheduling_confirmation():
    return render_template('Scheduling_Confirmation.html')

@app.route('/buildings', methods=['GET'])
def buildings():
    return render_template('Buildings.html')
    
@app.route('/building_confirmation', methods=['GET'])
def building_confirmation():
    return render_template('Building_Confirmation.html')
    
# api.add_resource(Facility, '/facilities', '/facilities/<f_id>')
# api.add_resource(Building, '/facilities/<f_id>/buildings', '/facilities/<f_id>/buildings/<b_id>')
api.add_resource(Room, '/facilities/<f_id>/buildings/<b_id>/rooms', '/facilities/<f_id>/buildings/<b_id>/rooms/<r_id>')
# api.add_resource(Room, '/rooms', '/rooms/<r_id>')
api.add_resource(Reservation, '/reservations', endpoint='reservation')
api.add_resource(User, '/users', '/users/<u_id>', endpoint='user')

if __name__ == '__main__':
    app.run(debug=True)
