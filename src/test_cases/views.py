from flask import Blueprint, jsonify, redirect, render_template, url_for

from src.qa.models import Question
from src.test_cases import TestAnswer, TestCase
from src.test_cases.serializers import TestCaseAnswerSchema, TestCaseSchema
from src.views import BaseView

bp = Blueprint('test_cases', __name__, template_folder='templates')


class TestCaseIndexView(BaseView):

    def get(self, question_id: str) -> tuple:
        if not Question.query.get(int(question_id)):
            return redirect(url_for('index.404'))

        return render_template(self.template_name, **self.context), 200


class TestCaseJsonView(BaseView):

    def get(self, question_id: str) -> tuple:
        schema: TestCaseSchema = TestCaseSchema()

        return jsonify(
            schema.dump(
                TestCase.query.filter(TestCase.question_id == int(question_id)).first(),
            ),
        ), 200


class TestAnswerView(BaseView):

    def get(self, answer_id: str) -> tuple:
        schema: TestCaseAnswerSchema = TestCaseAnswerSchema()

        test_answer: TestAnswer = TestAnswer.query.get(int(answer_id))

        if test_answer:
            return jsonify(
                schema.dump(test_answer),
            ), 200

        return jsonify({'error': 'answer not found'}), 404


bp.add_url_rule(
    '/testcase/<question_id>',
    view_func=TestCaseIndexView.as_view(
        name='test_case_index',
        template_name='test_case.jinja2',
    ),
)

bp.add_url_rule(
    '/api/testcase/<question_id>',
    view_func=TestCaseJsonView.as_view(
        name='test_case_json',
        template_name='',
    ),
)


bp.add_url_rule(
    '/api/testanswer/<answer_id>',
    view_func=TestAnswerView.as_view(
        name='test_answer',
        template_name='',
    ),
)
