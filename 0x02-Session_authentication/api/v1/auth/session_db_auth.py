#!/usr/bin/env python3
"""Module that contains the SessionDBAuth class"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm.exc import NoResultFound


class SessionDBAuth(SessionExpAuth):
    """sessiondbauth class"""
    def __init__(self):
        super().__init__()

    def create_session(self, user_id=None):
        """creates a session to be stored in a database"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        # Create a new UserSession instance and store it in the database
        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """gets session from the database based on the user_id"""
        if session_id is None:
            return None

        try:
            # Query the database for UserSession based on session_id
            user_session = UserSession.search({'session_id': session_id})

            if user_session:
                return user_session[0].user_id
        except Exception:
            return None

        return None

    def destroy_session(self, request=None):
        """destroys a session from the database"""
        if request is None:
            return False

        # Get the session ID from the request's cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        try:
            user_session = UserSession.search({'session_id': session_id})

            if user_session:
                user_session[0].remove()
                return True
        except Exception:
            pass
        return False
