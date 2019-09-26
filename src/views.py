from flask import Blueprint, render_template, session, current_app
from flask.views import MethodView

bp: Blueprint = Blueprint('index', __name__, template_folder='templates')


class BaseView(MethodView):

    def __init__(self, template_name):
        self.context = {
            'APP_NAME': current_app.config['APP_NAME']
        }
        self.template_name: str = template_name


class IndexPage(BaseView):

    def get(self):
        self.context.update(dict(auth=session.get('auth')))
        return render_template(self.template_name, **self.context)


bp.add_url_rule(
    '/',
    view_func=IndexPage.as_view(name='index', template_name='index.jinja2')
)
