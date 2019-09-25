from faker import Faker
from faker.generator import Generator
from flask import url_for

from tests.base import BaseTest


class TestRegistrationView(BaseTest):

    def test_registration(self):
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
