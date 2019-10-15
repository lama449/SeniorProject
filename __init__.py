from flask import Flask
import os

def create_app():
    #app = Flask(__name__)
    from SeniorProject.app import app
    app.secret_key = os.urandom(32)
    return app
