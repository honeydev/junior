from flask import url_for

from src.faq.models import Question
from tests.base import BaseTest
from tests.test_uttils import load_yaml_fixture


class TestIndexView(BaseTest):

    def test(self):
        response = self.client.get(url_for('.index'))
        self.assert200(response)


class TestQuestionsView(BaseTest):

    def setUp(self):
        super().setUp()
        fixtures: list[dict] = load_yaml_fixture('test_questions_view.yaml')

        self.questions: tuple[Question] = tuple()

        for fixture in fixtures:
            question: Question = Question()
            question.text = fixture['text']
            question.save()
            self.questions += (question,)

    def test(self):
        response = self.client.get(url_for('.index'))

        for question in self.questions:
            self.assertIn(question.text, str(response.data))
