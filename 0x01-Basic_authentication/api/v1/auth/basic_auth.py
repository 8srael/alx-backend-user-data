#!/usr/bin/env python3

""" basic authentication module """

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """ extract base64 authorization header """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """ decode base64 authorization header """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            return (base64.b64decode(base64_authorization_header)
                    .decode('utf-8'))
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """ extract user credentials
            Returns email and password
            from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """ user object """
        if (user_email is None or
                not isinstance(user_email, str) or
                user_pwd is None or
                not isinstance(user_pwd, str)):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_base64_auth_header is None:
            return None
        user_credentials = self.extract_user_credentials(
            decoded_base64_auth_header)
        if user_credentials is None:
            return None
        user = self.user_object_from_credentials(
            user_credentials[0],
            user_credentials[1])
        return user
