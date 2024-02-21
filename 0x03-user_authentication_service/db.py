#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a new user to db"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        user = self._session.query(User).filter_by(email=email).first()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the given keyword arguments
        """
        users = self._session.query(User)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in users:
                if getattr(user, key) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user by the given user_id
        """
        try:
            user = self._session.query(User).filter_by(id=user_id).first()
            for key, value in kwargs.items():
                if key not in user.__dict__:
                    raise ValueError
                setattr(user, key, value)
        except NoResultFound:
            raise ValueError
