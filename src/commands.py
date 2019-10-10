import click
from flask.cli import with_appcontext

from src.extensions import db
from src.qa.models import Chapter, Question
from src.user import User
from src.uttils import load_fixture


@click.command()
@with_appcontext
def load_chapters_questions():
    Question.query.delete()
    Chapter.query.delete()
    fixtures: dict = load_fixture('chapters-questions.yml')
    db.session.add_all(
        Chapter(**chapter_fixture)
        for chapter_fixture in fixtures['chapters']
    )

    db.session.add_all(
        Question(**question_fixture)
        for question_fixture in fixtures['questions']
    )

    db.session.commit()

    print('Chapters and questions successful load in database.')  # noqa TOO1


@click.option('-l', '--login')
@click.option('-p', '--password')
@click.option('-e', '--email')
@click.command()
@with_appcontext
def create_admin_user(login, password, email):
    password = User.hash_password(password)
    user = User(
        login=login,
        email=email,
        password=password.decode(),
        is_superuser=True,
    )
    User.save(user)

    print(f"Admin user created! {login} {email}.")  # noqa TOO1
