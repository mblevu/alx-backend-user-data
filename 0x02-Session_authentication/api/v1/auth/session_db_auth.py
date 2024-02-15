#!/usr/bin/env python3
"""implement session authentication"""
from api.v1.auth.auth import Auth
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user import User
import uuid


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """create a session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return
        user = User.get(user_id)
        if user is None:
            return
        user.session_id = session_id
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return
        user = User.search({'session_id': session_id})
        if user:
            return user[0].id
        return

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user = User.search({'session_id': session_id})
        if user:
            user = user[0]
            del user.session_id
            user.save()
            return True
        return False
