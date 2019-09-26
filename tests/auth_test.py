from faker import Faker
from faker.generator import Generator
from flask import url_for

from src.user.auth import GithubAuth
from src.user.models import User
from tests.base import BaseTest
from tests.mocks import get_github_profile_mock
from tests.test_utils import load_yaml_fixture


class TestRegistrationView(BaseTest):

    def test(self):
        factory: Generator = Faker()
        username: str = factory.user_name()
        password: str = factory.password()
        password_confirmation: str = password
        email: str = factory.email()
        first_name: str = factory.first_name()

        response = self.client.post(url_for('auth.registration'), data={
            'login': username,
            'password': password,
            'password_confirmation': password_confirmation,
            'email': email,
            'firstname': first_name
        })
        self.assert_redirects(response, url_for('auth.login'))


class TestGithubAuthRedirect(BaseTest):

    def test(self):
        response = self.client.get(url_for('github.login'))
        self.assert_status(response, 302)


class TestGithubAuthCreateNewUser(BaseTest):

    def test(self):
        github_profile: dict = get_github_profile_mock()
        github_auth: GithubAuth = GithubAuth.create(github_profile)
        user: User = github_auth.auth_user
        self.assertEqual(user.email, github_profile['email'])
        self.assertEqual(user.login, github_profile['login'])


class TestGithubAuthWithExistUser(BaseTest):

    def setUp(self):
        super().setUp()
        fixture: dict = load_yaml_fixture('auth_test_existed_github_user.yaml')
        self.user: User = User(email=fixture['email'], login=fixture['login'])
        self.user.id = fixture['id']
        self.user.save()

    def test(self):
        github_auth: GithubAuth = GithubAuth.create({
            'email': self.user.email,
            'login': self.user.login
        })

        self.assertTrue(github_auth.auth_user.email, self.user.email)
        self.assertTrue(github_auth.auth_user.login, self.user.login)
        self.assertTrue(github_auth.auth_user.id, self.user.id)
