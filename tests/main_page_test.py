from flask import url_for

from src.extensions import db
from src.qa.models import Chapter, Question
from src.uttils import load_fixture
from tests.base import BaseTest


class TestIndexView(BaseTest):

    def test(self):
        response = self.client.get(url_for('.index'))
        self.assert200(response)


class TestQuestionsView(BaseTest):

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

    def test(self):
        response = self.client.get(url_for('.index'))
        parsed_response: str = response.data.decode('utf-8')

        for chapter in self.chapters:
            self.assertIn(chapter.name, parsed_response)

        for question in self.questions:
            self.assertIn(question.text, parsed_response)
            self.assertIn(str(question.order_number), parsed_response)
