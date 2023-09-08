#!/usr/bin/env python3

"""Session authentication module"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on session ID """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
