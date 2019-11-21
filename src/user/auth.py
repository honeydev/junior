from http import HTTPStatus

from flask import current_app as junior_app
from flask import session
from flask_dance.contrib.github import github

from src.user.models import User
from src.user.uttils import get_or_create_user_through_github


def auth_hook() -> None:
    current_session: SessionAuth or bool = session.get('auth', False)

    if github.authorized:
        session['auth'] = GithubAuth.create(github.get('user').json())
    else:
        current_session or session.update(dict(auth=SessionAuth(False)))  # noqa WPS428


class BaseAuth:

    def __init__(self, auth: bool, user: User = None, ouath_data: dict = None):
        self.auth: bool = auth
        self.user: User = user
        self.ouath_data: dict = ouath_data

    def __bool__(self) -> bool:
        return self.auth

    def logout(self) -> None:
        session['auth'] = SessionAuth(False)


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
    def is_oauth(self) -> bool:
        return True

    def logout(self, github_client=github) -> None:

        client_id: str = github_client.client_id
        access_token: str = github_client.access_token
        client_secret: str = github_client.blueprint.client_secret

        response = github_client.delete(
            f'/applications/{client_id}/grants/{access_token}',
            auth=(client_id, client_secret))

        if response.status_code != HTTPStatus.NO_CONTENT:
            raise RuntimeError('Github logout error')
        # log out nethod writen in flask-dance documentation
        del junior_app.blueprints['github'].token  # noqa WPS420

        super().logout()

    @classmethod
    def create(cls, github_profile: dict) -> BaseAuth:
        user = get_or_create_user_through_github(github_profile)
        if user:
            return cls(True, user, github_profile)
        return cls(False)
