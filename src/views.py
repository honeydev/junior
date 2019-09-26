from flask import Blueprint, render_template, session
from flask.views import MethodView

bp: Blueprint = Blueprint('index', __name__, template_folder='templates')


class IndexPage(MethodView):

    def __init__(self, template_name):
        self.template_name: str = template_name

    def get(self):
        context = dict(auth=session.get('auth'))
        return render_template(self.template_name, **context)


bp.add_url_rule(
    '/',
    view_func=IndexPage.as_view(name='index', template_name='index.jinja2')
)
