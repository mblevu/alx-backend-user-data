#!/usr/bin/env python3
"""basic auth inheritance"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """class to manage the API authentication.
    Inherits from Auth."""
    def __init__(self) -> None:
        """init method"""
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode(
                'utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        if user_email is None or not str:
            return None
        if user_pwd is None or not str:
            return None

        users = User.search({'email': user_email})
        if not users:
            return
        users = users[0]
        if not users.is_valid_password(user_pwd):
            return None
        return users
