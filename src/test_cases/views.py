from flask import Blueprint, jsonify, redirect, render_template, url_for

from src.qa.models import Question
from src.test_cases import TestCase, TestQuestionUserRelation
from src.test_cases.services import TestCaseService
from src.user.decorators import login_required_user
from src.views import BaseView

bp = Blueprint('test_cases', __name__, template_folder='templates')


class TestCaseIndexView(BaseView):

    def get(self, question_id: str) -> tuple:
        if not Question.query.get(int(question_id)):
            return redirect(url_for('index.404'))

        return render_template(self.template_name, **self.context), 200


class TestCaseJsonView(BaseView):

    @login_required_user
    def get(self, user, question_id: str) -> tuple:

        service = TestCaseService(
            user,
            TestCase.query.filter(TestCase.question_id == int(question_id)).first(),
        )

        return jsonify(service.load_user_case()), 200


class FinalizeTestQuestion(BaseView):

    @login_required_user
    def put(self, user, test_question_id: str):
        relation = TestQuestionUserRelation.query.filter(
            TestQuestionUserRelation.test_question_id == test_question_id,
            TestQuestionUserRelation.user_id == user.id,
        ).first()

        relation.completed = True
        relation.save()

        return jsonify({'success': True}), 200


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
    '/api/testcase/finalize-question/<test_question_id>',
    view_func=FinalizeTestQuestion.as_view(
        name='finalize_question',
        template_name='',
    ),
)
