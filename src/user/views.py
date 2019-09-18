from hashlib import sha256

from flask import Blueprint, Flask, render_template, request
from flask.views import MethodView


user_bp = Blueprint('auth', __name__, template_folder='templates')

app = Flask(__name__, )


class Registration(MethodView):

    def __init__(self, template_name):
        self.template_name: str = template_name

    def post(self):
        """Регистрация."""
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2:
            sha256(password.encode()).hexdigest()

    def get(self):
        """Форма регистрации."""
        return render_template(self.template_name)


user_bp.add_url_rule(
    '/auth/', view_func=Registration.as_view(
        name='auth', template_name='register_form.jinja2'
    )
)
