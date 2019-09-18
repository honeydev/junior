from flask import Blueprint, render_template
from flask.views import MethodView


index_bp: Blueprint = Blueprint('index', __name__, template_folder='templates')


class IndexPage(MethodView):

    def __init__(self, template_name):
        self.template_name: str = template_name

    def get(self):
        return render_template(self.template_name)


index_bp.add_url_rule(
    '/',
    view_func=IndexPage.as_view(name='index', template_name='index.jinja2')
)
