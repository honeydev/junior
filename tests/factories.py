from faker import Faker
from flask import url_for

from src.user.models import User

factory = Faker()


def create_user(save=True):

    password = factory.password(10)
    user = User(
        login=factory.user_name(),
        email=factory.email(),
        password=User.hash_password(password),
        firstname=factory.first_name(),
        middlename=factory.name(),
        lastname=factory.last_name(),
        is_aproved=True,
    )

    if save:
        user.save()

    return user, password


def create_auth_user(test_client):
    user, password = create_user()

    res = test_client.post(
        url_for('auth.login'),
        data=dict(login=user.login, password=password),
    )

    session_id = res.headers['Set-Cookie'].split(' ')[0].split('=')[1]
    test_client.set_cookie('http://localhost/', 'session', session_id)

    return user, session_id
