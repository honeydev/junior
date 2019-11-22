import click
from flask.cli import with_appcontext

from src.extensions import db
from src.qa.models import Answer, Chapter, Question, Section
from src.user import User
from src.uttils import load_fixture


@click.command()
@with_appcontext
def clear_questions():
    """Clear all Sections, Chapters, Questions."""
    Answer.query.delete()
    Question.query.delete()
    Chapter.query.delete()
    Section.query.delete()

    db.session.commit()

    print('DB cleared successfully') # noqa TOO1


@click.command()
@click.argument('fixture_name')
@with_appcontext
def load_section_questions(fixture_name: str):
    """
    Load selected Section, related Chapters and Questions.

    Requires YML filename without '-questions.yml'
    Example:
    flask load-section-questions bars
    """
    fixtures: dict = load_fixture(f'{fixture_name}-questions.yml')
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

    print(f'{fixture_name}: chapters and questions successful load in database.')  # noqa TOO1


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
