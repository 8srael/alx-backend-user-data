#!/usr/bin/env python3
"""model for the user sessions"""
from models.base import Base


class UserSession(Base):
    """the user session class"""

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
