from flask import Blueprint, current_app, render_template, session
from flask.views import MethodView

from src.qa.models import Chapter

bp: Blueprint = Blueprint('index', __name__, template_folder='templates')


class BaseView(MethodView):

    def __init__(self, template_name):
        self.context = {
            'auth': session.get('auth'),
            'app_name': current_app.config['APP_NAME'],
        }
        self.template_name: str = template_name


class IndexPage(BaseView):

    def get(self):

        self.context.update(
            dict(
                chapters=Chapter.query.all(),
            ),
        )
        return render_template(self.template_name, **self.context)


class NotFoundPage(BaseView):

    def get(self):
        return render_template(self.template_name, **self.context)


bp.add_url_rule(
    '/',
    view_func=IndexPage.as_view(name='index', template_name='index.jinja2'),
)

bp.add_url_rule(
    '/',
    view_func=IndexPage.as_view(name='404', template_name='404.jinja2'),
)
