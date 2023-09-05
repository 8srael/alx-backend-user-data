#!/usr/bin/env python3

""" basic authentication module """

from api.v1.auth.auth import Auth


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
