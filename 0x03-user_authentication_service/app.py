#!/usr/bin/env python3

""" Basic Flask app """

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return:
      - JSON payload : {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """ POST /users
    Return:
        - JSON payload : {"email": "<user email>", "message": "user created"}
                                or
        - JSON payload : {"email already registered"} with
                            400 - Bad Reqquest HTTP status
    """
    email = request.form.get("email")
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    Return:
        - JSON payload : {"email": "<user email>", "message": "logged in"}
                                    or
        - 401 - Unauthorized HTTP status
    """
    email = request.form.get("email")
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /sessions
    Return:
        - Redirect to /
                or
        - 403 - Forbidden HTTP status
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
        GET /profile
        Return:
            - JSON payload : {"email": "<user email>"}
                            or
            - 403 - Forbidden HTTP status
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
