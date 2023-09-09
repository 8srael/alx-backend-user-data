#!/usr/bin/env python3
""" Module of Session authentication views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route(
    '/auth_session/login/',
    methods=['POST'], strict_slashes=False
)
def session_login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User instance based on the email
    """
    if request.form.get('email') is None:
        return jsonify({"error": "email missing"}), 400
    if request.form.get('password') is None:
        return jsonify({"error": "password missing"}), 400
    requestEmail = request.form.get('email')
    requestPwd = request.form.get('password')
    users = User.search({'email': requestEmail})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(requestPwd):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
    out = jsonify(user.to_json())
    out.set_cookie(os.getenv('SESSION_NAME', '_my_session_id'), session_id)
    return out


@app_views.route(
    '/auth_session/logout/',
    methods=['DELETE'], strict_slashes=False)
def session_logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - If destroy_session returns False, abort(404)
      -  Otherwise, return an empty JSON dictionary with the status code 200
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
