#!/usr/bin/env python3
"""module that contains the session authentication class
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """session expiration class"""
    def __init__(self):
        super().__init__()
        session_duration_str = getenv('SESSION_DURATION', '0')
        try:
            self.session_duration = int(session_duration_str)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Call the create_session method of the parent class (SessionAuth)"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        # Create a session dictionary
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        # Set the session dictionary in user_id_by_session_id
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """some function"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')

        if created_at is None:
            return None

        current_time = datetime.now()
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if current_time > expiration_time:
            return None

        return session_dict.get('user_id')
