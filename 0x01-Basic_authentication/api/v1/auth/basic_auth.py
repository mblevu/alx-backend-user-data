#!/usr/bin/env python3
"""basic auth inheritance"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class to manage the API authentication.
    Inherits from Auth."""
    def __init__(self) -> None:
        """initialize the basic auth"""
        pass
