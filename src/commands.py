import click
from flask.cli import with_appcontext

from src.extensions import db
from src.qa.models import Chapter, Question
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
