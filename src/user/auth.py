from flask import session
from flask_dance.contrib.github import github

from src.user.models import User
from src.user.utils import get_or_create_user_through_github


def auth_hook() -> None:
    current_session: SessionAuth or bool = session.get('auth', False)

    if github.authorized:
        session['auth'] = GithubAuth.create(github.get('user').json())
    else:
        current_session or session.update(dict(auth=SessionAuth(False)))


class BaseAuth:

    def __init__(self, auth: bool, user: User = None, ouath_data: dict = {}):
        self.auth: bool = auth
        self.user: User = user
        self.ouath_data: dict = ouath_data


class SessionAuth(BaseAuth):

    @property
    def auth_user(self) -> User:
        return self.user

    @property
    def is_oauth(self) -> bool:
        return False


class GithubAuth(BaseAuth):

    @property
    def auth_user(self) -> User:
        return self.user

    @property
    def is_oauth() -> bool:
        return True

    @classmethod
    def create(cls, github_profile: dict) -> BaseAuth:
        user = get_or_create_user_through_github(github_profile)
        return cls(True, user, github_profile)
