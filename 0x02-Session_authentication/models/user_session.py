#!/usr/bin/env python3
"""User session module"""
from models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class UserSession(Base):
    """stores user session information"""
    __tablename__ = 'user_sessions'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(60), nullable=False)
    user = relationship("User", back_populates="session")

    def __init__(self, *args: list, **kwargs: dict):
        """initializes user session"""
        super().__init__(*args, **kwargs)
        self.session_id = os.getenv('SESSION_ID')
        self.user_id = os.getenv('USER_ID')
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        else:
            super().__init__()
