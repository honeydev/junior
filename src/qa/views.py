from flask import Blueprint, redirect, render_template, request, session

from src.qa.forms import AnswerForm
from src.qa.models import Answer, Question
from src.views import BaseView

bp: Blueprint = Blueprint('answers', __name__, template_folder='templates')


class AnswerView(BaseView):

    def get_context(self, question_id):
        question = Question.query.get(question_id)
        answers = Answer.query.filter_by(
            question_id=question_id,
        ).all()
        if request.method == 'GET':
            form = AnswerForm()
        else:
            form = AnswerForm(request.form)
        self.context.update(
            dict(
                auth=session.get('auth'),
                question=question,
                answers=answers,
                form=form,
            ),
        )
        return self.context

    def get(self, question_id):
        self.context.update(
            self.get_context(question_id),
        )
        return render_template(self.template_name, **self.context)

    def post(self, question_id):
        self.context.update(
            self.get_context(question_id),
        )

        if not self.context['form'].validate():
            return render_template(
                self.template_name,
                **self.context,
            )
        if self.context['form'].text.data:
            answer = Answer(
                text=self.context['form'].text.data,
                question_id=question_id,
            )
            Answer.save(answer)
        return redirect(request.url)


bp.add_url_rule(
    '/answer/<int:question_id>/',
    view_func=AnswerView.as_view(
        name='answer', template_name='answer.jinja2',
    ),
)
