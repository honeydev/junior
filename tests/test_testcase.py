from flask import url_for

from src.extensions import db
from src.qa.models import Chapter, Question
from src.uttils import load_fixture
from tests.base import BaseTest


class TestIndexView(BaseTest):

    def setUp(self):
        super().setUp()
        fixtures: list[dict] = load_fixture('chapters-questions.yml')

        self.questions: tuple = tuple(
            Question(**question_fixture).save()
            for question_fixture in fixtures['questions']
        )

        self.chapters: tuple = tuple(
            Chapter(**chapter_fixture)
            for chapter_fixture in fixtures['chapters']
        )

        db.session.add_all(self.questions)
        db.session.add_all(self.chapters)

    def test_found(self):
        response = self.client.get(
            url_for('test_cases.test_case', question_id=self.questions[1].id),
        )
        self.assert200(response)

    def test_not_found(self):
        not_found_value = -1
        response = self.client.get(
            url_for('test_cases.test_case', question_id=not_found_value),
        )
        self.assert_redirects(response, url_for('index.404'))
