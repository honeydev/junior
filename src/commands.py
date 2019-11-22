import click
from flask.cli import with_appcontext

from src.extensions import db
from src.qa.models import Answer, Chapter, Question, Section
from src.user import User
from src.uttils import load_fixture


@click.command()
@with_appcontext
def db_clear_questions():
    """
    Clear Sections, Chapters, Questions
    """
    Answer.query.delete()
    Question.query.delete()
    Chapter.query.delete()
    Section.query.delete()

    db.session.commit()

    print('DB cleared successfully')


@click.command()
@with_appcontext
def load_minimum_questions():
    """
    Load Minimum, related Chapters and Questions
    """

    fixtures: dict = load_fixture('minimum-questions.yml')
    db.session.add_all(
        Chapter(**chapter_fixture)
        for chapter_fixture in fixtures['chapters']
    )
    db.session.add_all(
        Question(**question_fixture)
        for question_fixture in fixtures['questions']
    )

    db.session.add_all(
        Section(**section_fixture)
        for section_fixture in fixtures['sections']
    )

    db.session.commit()

    print('Minimum: chapters and questions successful load in database.')  # noqa TOO1


@click.command()
@with_appcontext
def load_bars_questions():
    """
    Load Bars, related Chapters and Questions
    """

    fixtures: dict = load_fixture('bars-questions.yml')
    db.session.add_all(
        Chapter(**chapter_fixture)
        for chapter_fixture in fixtures['chapters']
    )
    db.session.add_all(
        Question(**question_fixture)
        for question_fixture in fixtures['questions']
    )

    db.session.add_all(
        Section(**section_fixture)
        for section_fixture in fixtures['sections']
    )

    db.session.commit()

    print('Bars: chapters and questions successful load in database.')  # noqa TOO1


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
