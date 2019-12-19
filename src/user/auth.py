from flask import session

from src.user.models import User
from src.user.oauth import get_or_create_user_through_oauth


def auth_hook() -> None:

    session['auth'] = session.get('auth') if session.get('auth', False) else SessionAuth(False)


class SessionAuth:

    def __init__(self, auth: bool, user: User = None):
        self.auth: bool = auth
        self._user: User = user

    def __bool__(self) -> bool:
        return self.auth

    def logout(self) -> None:
        session['oauth_link'] = False
        session['oauth_new'] = False
        session['auth'] = SessionAuth(False)

    @property
    def user(self) -> User:
        return User.query.get(self._user.id)

    @classmethod
    def create_from_oauth(cls, service: str, profile: dict):
        user = get_or_create_user_through_oauth(service, profile)
        if user:
            # FIXME: без запроса к БД падает после создании юзера DetachedInstanceError
            return cls(True, User.query.get(user.id))
        return cls(False)
