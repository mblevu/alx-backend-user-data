#!/usr/bin/env python3
"""session expiration"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session expiration class"""

    def __init__(self) -> None:
        """Constructor method"""
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id: str = None) -> str:
        """Create session method"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """User id for session id method"""
        if session_id is None:
            return None
        session_dict = super().user_id_for_session_id(session_id)
        if session_dict is None:
            return None
        if 'created_at' not in session_dict:
            return None
        if 'user_id' not in session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict['user_id']
        before_time = session_dict[
            'created_at'] + timedelta(seconds=self.session_duration)
        if before_time < datetime.utcnow():
            return None
        return session_dict['user_id']
