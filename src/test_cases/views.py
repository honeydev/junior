from flask import Blueprint, redirect, render_template, url_for

from src.qa.models import Question
from src.views import BaseView

bp = Blueprint('test_cases', __name__, template_folder='templates')


class TestCase(BaseView):

    def get(self, question_id: str):
        if not Question.query.get(int(question_id)):
            return redirect(url_for('index.404'))

        return render_template(self.template_name, **self.context)


bp.add_url_rule(
    '/testcase/<question_id>',
    view_func=TestCase.as_view(
        name='test_case',
        template_name='test_case.jinja2',
    ),
)
