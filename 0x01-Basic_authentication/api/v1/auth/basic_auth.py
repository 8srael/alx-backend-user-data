#!/usr/bin/env python3

""" basic authentication module """

from api.v1.auth.auth import Auth
import base64


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
