#!/usr/bin/env python3
"""basic auth inheritance"""
import base64
from api.v1.auth.auth import Auth


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
            self, decoded_base64_authorization_header: str) -> (str, str): # type: ignore
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1])
