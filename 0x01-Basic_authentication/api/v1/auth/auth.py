#!/usr/bin/env python3

""" Module for API authentication """

from flask import request


class Auth():
    """ manages API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method"""
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization_header method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method"""
        return None
