from flask import Flask

def create_app():
    app = Flask(__name__)
    from SeniorProject.app import app
    return app
