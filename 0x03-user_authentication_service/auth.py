#!/usr/bin/env python3
""" auth module """

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """
        Returns a salted hash of password
    """
    return hashpw(password.encode('utf-8'), gensalt())
