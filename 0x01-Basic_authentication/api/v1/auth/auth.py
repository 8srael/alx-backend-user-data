#!/usr/bin/env python3

""" Module for API authentication """

from flask import request
from typing import List, TypeVar


class Auth():
    """ manages API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method
            define which routes don't need authentication
            return True if the route is not listed in excluded_paths
            False otherwise
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if (excluded_path.endswith('*')
                    and path.startswith(excluded_path[:-1])):
                return False
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header method"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method"""
        return None
