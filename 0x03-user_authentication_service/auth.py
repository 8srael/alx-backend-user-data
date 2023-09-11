#!/usr/bin/env python3
""" auth module """

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """ Returns a salted hash of password """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """ Returns a string representation of a new UUID """
    return str(uuid.uuid4())


class Auth:
    """
        Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
            Registers and returns a new user if email isn’t listed
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(user.email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if a user exists and validates credentials """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Creates a session ID for a user """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
