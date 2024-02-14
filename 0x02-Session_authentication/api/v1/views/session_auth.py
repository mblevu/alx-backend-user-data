#!/usr/bin/env python3
"""handles all routes for session authentication"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from api.v1.auth.session_auth import SessionAuth
from os import getenv

sa = SessionAuth()
SESSION_NAME = getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """logs in a user"""
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """logs out a user"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
