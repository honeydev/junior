from flask import Blueprint, redirect, render_template, request, session
from sqlalchemy import desc

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
        ).order_by(desc('likes_count'))
        buttons_status = dict()
        if session.get('auth'):
            user_id = session.get('auth').user.id
            ans_user_relations = AnswerUsersRelations.query.filter_by(
                user_id=user_id).values('answer_id', 'set_like')
            ans_user_relations = {answer_id: set_like for answer_id, set_like in ans_user_relations}
            buttons_status = {
                answer.id: get_buttons_status(ans_user_relations, answer)
                for answer in answers
            }

        self.context.update(
            dict(
                auth=session.get('auth'),
                question=question,
                answers=answers,
                button_status=buttons_status,
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
            owner_id=session['auth'].user.id,
        )
        Answer.save(answer)
        return redirect(request.url)


class LikesCountView(BaseView):

    def post(self, answer_id, like):
        try:
            user_id = session['auth'].user.id
        except AttributeError:
            return redirect('/')
        answer = Answer.query.get({'id': answer_id})
        ans_user_relations = AnswerUsersRelations.query.filter_by(
            answer_id=answer_id, user_id=user_id)

        if not ans_user_relations.count():  # noqa:WPS504
            ans_user_rel = AnswerUsersRelations(
                user_id=user_id,
                answer_id=answer_id,
                set_like=bool(like),
            )
            AnswerUsersRelations.save(ans_user_rel)
            answer.update_likes_count(like, on_created=True)
        else:   # noqa:WPS513
            if like and not ans_user_relations.value('set_like'):
                ans_user_relations.update({'set_like': True})
                answer.update_likes_count(like)
            elif like == 0 and ans_user_relations.value('set_like'):
                ans_user_relations.update({'set_like': False})
                answer.update_likes_count(like)

        return redirect(request.referrer)


def get_buttons_status(ans_user_relations, answer):
    bootstrap = [
        'data-toggle="tooltip"',
        'data - placement = "right"',
        'title = "Вы уже проголосовали."',
        'disabled',
    ]

    button_colors = {
        True: {
            'like': ' '.join(bootstrap),
            'dislike': '',
        },
        False: {
            'like': '',
            'dislike': ' '.join(bootstrap),
        },
        'default': {
            'like': '',
            'dislike': '',
        },
    }
    for answer_id, set_like in ans_user_relations.items():
        if answer.id == answer_id:
            return button_colors[set_like]
    return button_colors['default']


bp.add_url_rule(
    '/answer/<int:question_id>/',
    view_func=AnswerView.as_view(
        name='answer', template_name='answer.jinja2',
    ),
)


bp.add_url_rule(
    '/answer/<int:answer_id>/like=<int:like>/',
    view_func=LikesCountView.as_view(
        name='likes_count', template_name='answer.jinja2',
    ),
)
