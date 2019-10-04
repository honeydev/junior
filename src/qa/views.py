from flask import Blueprint, render_template
from flask.views import MethodView

bp = Blueprint('qa', __name__, template_folder='templates')


class Answers(MethodView):
    def __init__(self, template_name):
        self.template: str = template_name

    def get(self):
        return render_template(self.template)


bp.add_url_rule(
    '/qa/',
    view_func=Answers.as_view(
        name='qa',
        template_name='FAQ_page.jinja2',
    ),
)
