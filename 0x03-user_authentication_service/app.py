#!/usr/bin/env python3
"""Basic flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register a user"""
    email = ''
    password = ''
    try:
        email = request.form['email']
    except KeyError:
        return jsonify({"message": "email required"}), 400
    try:
        password = request.form['password']
    except KeyError:
        return jsonify({"message": "password required"}), 400
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login a user"""
    email = ''
    password = ''
    try:
        email = request.form['email']
    except KeyError:
        return jsonify({"message": "email required"}), 400
    try:
        password = request.form['password']
    except KeyError:
        return jsonify({"message": "password required"}), 400
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response, 200
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logout a user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/', code=302)
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
