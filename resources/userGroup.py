# userGroup.py
# Endpoints for managing maintenance requests
# Monica Mahon, 11/26/2019

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Resource, request
import bcrypt
from SeniorProject import database
from bson.objectid import ObjectId

class UserGroup(Resource):
    def get(self, f_id, g_id=None):
        pass

    def post(self, f_id):
        pass

    def put(self, f_id, g_id):
        pass

    def delete(self, f_id, g_id):
        pass
