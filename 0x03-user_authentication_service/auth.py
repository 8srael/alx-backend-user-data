#!/usr/bin/env python3
""" auth module """

from bcrypt import hashpw, gensalt
from db import DB
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Returns a salted hash of password """
    return hashpw(password.encode('utf-8'), gensalt())


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
