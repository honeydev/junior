from flask import url_for

from src.extensions import db
from src.qa.models import Chapter, Question, Section
from src.test_cases import TestCase, TestQuestion
from src.uttils import load_fixture
from tests.base import BaseTest
from tests.factories import create_auth_user
from tests.test_uttils import load_yaml_fixture


class FinalizeTestQuestion(BaseTest):
    """Тест экшена для успешнго завершения тестового задания."""

    def setUp(self):
        super().setUp()
        fixtures: list[dict] = load_fixture('minimum-questions.yml')
        test_cases_fixtures: dict = load_yaml_fixture('test_cases.yaml')

        self.questions: tuple = tuple(
            Question(**question_fixture).save()
            for question_fixture in fixtures['questions']
        )

        self.chapters: tuple = tuple(
            Chapter(**chapter_fixture)
            for chapter_fixture in fixtures['chapters']
        )

        self.sections: tuple = tuple(
            Section(**section_fixture)
            for section_fixture in fixtures['sections']
        )

        self.test_cases: tuple = tuple(
            TestCase(**test_case_fixture)
            for test_case_fixture in test_cases_fixtures['test_cases']
        )

        self.test_questions: tuple = tuple(
            TestQuestion(**test_question)
            for test_question in test_cases_fixtures['test_questions']
        )

        db.session.add_all(self.sections)
        db.session.add_all(self.chapters)
        db.session.add_all(self.questions)
        db.session.add_all(self.test_cases)
        db.session.add_all(self.test_questions)

    def test(self):
        create_auth_user(self.client)

        test_case = self.client.get(
            url_for('test_cases.test_case_json', question_id=self.questions[0].id),
        ).json

        response = self.client.put(
            url_for(
                'test_cases.finalize_question',
                test_question_id=test_case[0]['id'],
            ),
        )

        parsed_response = response.json

        test_case_updated = self.client.get(
            url_for('test_cases.test_case_json', question_id=self.questions[0].id),
        ).json

        self.assert200(response)
        self.assertTrue(parsed_response['success'])
        self.assertTrue(test_case_updated[0]['completed'])
