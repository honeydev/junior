from flask import Blueprint, redirect, render_template, request, session

from src.qa.forms import AnswerForm
from src.qa.models import Answer, AnswerUsersRelations, Question
from src.user import LoginForm
from src.views import BaseView

bp: Blueprint = Blueprint('answers', __name__, template_folder='templates')


class AnswerView(BaseView):

    def get_context(self, question_id):
        question = Question.query.get(question_id)
        answers = Answer.query.filter_by(
            question_id=question_id,
        ).order_by('created')
        self.context.update(
            dict(
                auth=session.get('auth'),
                question=question,
                answers=answers,
            ),
        )
        return self.context

    def get(self, question_id):
        self.get_context(question_id)
        self.context['form'] = AnswerForm()
        self.context['login_form'] = LoginForm()
        return render_template(self.template_name, **self.context)

    def post(self, question_id):
        self.get_context(question_id)
        self.context['form'] = AnswerForm(request.form)
        if not self.context['form'].validate():
            return render_template(
                self.template_name,
                **self.context,
            )
        answer = Answer(
            text=self.context['form'].text.data,
            question_id=question_id,
        )
        Answer.save(answer)
        return redirect(request.url)


class LikesCountView(BaseView):

    def post(self, question_id, answer_id, like):
        answer = Answer.query.filter_by(
            question_id=question_id,
            id=answer_id).first()
        ans_user_relations = AnswerUsersRelations.query.filter_by(
            user_id=session['auth'].user.id,
            answer_id=answer_id).first()
        if not ans_user_relations:
            ans_user_rel = AnswerUsersRelations(
                user_id=session['auth'].user.id,
                answer_id=answer_id,
                set_like=0,
            )
            AnswerUsersRelations.save(ans_user_rel)
        ans_user_relations = AnswerUsersRelations.query.filter_by(
            user_id=session['auth'].user.id,
            answer_id=answer_id).first()
        if like == 'plus' and ans_user_relations.set_like < 1:
            answer.likes_count += 1
            ans_user_relations.set_like = 1
        if like == 'minus' and ans_user_relations.set_like > -1:
            answer.likes_count -= 1
            ans_user_relations.set_like = -1
        return redirect(request.referrer)


bp.add_url_rule(
    '/answer/<int:question_id>/',
    view_func=AnswerView.as_view(
        name='answer', template_name='answer.jinja2',
    ),
)


bp.add_url_rule(
    '/answer/<int:question_id>/<int:answer_id>/like=<string:like>/',
    view_func=LikesCountView.as_view(
        name='likes_count', template_name='answer.jinja2',
    ),
)
