from flask import Blueprint, make_response, redirect, render_template, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from .models import User


bp = Blueprint('auth', __name__, template_folder='templates')


class Registration(MethodView):

    def __init__(self, template_name):
        self.template_name: str = template_name

    def post(self):
        """Регистрация."""
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        pass_hash = User.hash_password(password)
        user = User(
            login=login,
            email=email,
            password=pass_hash,
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
        )
        if User.check_password(user, password_confirmation):
            try:
                user.save()
                result = redirect('/')
            except IntegrityError:
                result = make_response(('Юзер уже существует', 400))
        else:
            result = make_response(('Неверные данные', 400))
        return result

    def get(self):
        """Форма регистрации."""
        return render_template(self.template_name)


bp.add_url_rule(
    '/auth/', view_func=Registration.as_view(
        name='auth', template_name='register_form.jinja2'
    )
)
