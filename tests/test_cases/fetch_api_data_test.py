import json

from flask import url_for

from src.extensions import db
from src.qa.models import Chapter, Question
from src.test_cases import TestCase, TestQuestion
from src.test_cases.constants import AnswerTypes
from src.uttils import load_fixture
from tests.base import BaseTest
from tests.factories import create_auth_user
from tests.test_uttils import load_yaml_fixture


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
            url_for('test_cases.test_case_index', question_id=self.questions[1].id),
        )
        self.assert200(response)

    def test_not_found(self):
        not_found_value = -1
        response = self.client.get(
            url_for('test_cases.test_case_index', question_id=not_found_value),
        )
        self.assert_redirects(response, url_for('index.404'))


class TestFetchTestCaseData(BaseTest):

    def setUp(self):
        super().setUp()
        fixtures: list[dict] = load_fixture('chapters-questions.yml')
        test_cases_fixtures: dict = load_yaml_fixture('test_cases.yaml')

        self.questions: tuple = tuple(
            Question(**question_fixture).save()
            for question_fixture in fixtures['questions']
        )

        self.chapters: tuple = tuple(
            Chapter(**chapter_fixture)
            for chapter_fixture in fixtures['chapters']
        )

        self.test_cases: tuple = tuple(
            TestCase(**test_case_fixture)
            for test_case_fixture in test_cases_fixtures['test_cases']
        )

        self.test_questions: tuple = tuple(
            TestQuestion(**test_question)
            for test_question in test_cases_fixtures['test_questions']
        )

        db.session.add_all(self.chapters)
        db.session.add_all(self.questions)
        db.session.add_all(self.test_cases)
        db.session.add_all(self.test_questions)

    def test(self):

        test_case: TestCase = self.test_cases[0]

        create_auth_user(self.client)

        response = self.client.get(
            url_for('test_cases.test_case_json', question_id=test_case.question_id),
        )

        self.assert200(response)

        parsed_response: dict = json.loads(response.get_data())

        for test_question in self.test_questions:
            response_question = list(filter(
                lambda question: int(question['id']) == test_question.id,
                parsed_response,
            ))[0]

            self.assertEqual(
                response_question['question_type'],
                AnswerTypes.get_name(test_question.question_type).name.lower(),
            )
            self.assertEqual(response_question['text'], test_question.text)
