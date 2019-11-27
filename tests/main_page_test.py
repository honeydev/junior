from flask import url_for

from src.extensions import db
from src.qa.models import Chapter, Question, Section
from src.uttils import load_fixture
from tests.base import BaseTest


class TestIndexView(BaseTest):

    def setUp(self):
        super().setUp()
        load_question_structure(self)

    def test(self):
        response = self.client.get(url_for('index.home'))
        self.assert_redirects(response, url_for('index.index', section_id=1))


class TestQuestionsView(BaseTest):

    def setUp(self):
        super().setUp()
        load_question_structure(self)

    def test(self):
        response = self.client.get(url_for('index.index', section_id=1))
        parsed_response: str = response.data.decode('utf-8')
        max_index_page_len = 40

        for section in self.sections:
            self.assertIn(section.name, parsed_response)

        for chapter in self.chapters:
            self.assertIn(chapter.name, parsed_response)

        for question in self.questions:
            if len(question.text) > max_index_page_len:
                self.assertIn(question.text[:max_index_page_len], parsed_response)
            else:
                self.assertIn(question.text, parsed_response)
            self.assertIn(str(question.order_number), parsed_response)


def load_question_structure(self):
    fixtures: list[dict] = load_fixture('minimum-questions.yml')

    self.sections: tuple = tuple(
        Section(**section_fixture).save()
        for section_fixture in fixtures['sections']
    )

    self.chapters: tuple = tuple(
        Chapter(**chapter_fixture).save()
        for chapter_fixture in fixtures['chapters']
    )

    self.questions: tuple = tuple(
        Question(**question_fixture).save()
        for question_fixture in fixtures['questions']
    )

    db.session.add_all(self.questions)
    db.session.add_all(self.chapters)
    db.session.add_all(self.sections)
