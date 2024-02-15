#!/usr/bin/env python3
"""manage the API authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        for p in excluded_paths:
            if p.endswith('*') and path.startswith(p[:-1]):
                return False
        return True

