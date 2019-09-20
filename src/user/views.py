from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    session,
)
from flask.views import MethodView

from .models import User


bp = Blueprint('auth', __name__, template_folder='templates')


class Registration(MethodView):

    def __init__(self, template_name):
        self.template_name: str = template_name

    def post(self):
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
            password=pass_hash.decode(),
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
        )
        if User.check_password(user, password_confirmation):
            if User.query.filter_by(login=login, email=email).first():
                result = make_response(('Логин или Email уже заняты.', 400))
            else:
                User.save(user)
                result = redirect('/')
        else:
            result = make_response(('Неверные данные', 400))
        return result

    def get(self):
        return render_template(self.template_name)


class Login(MethodView):
    def __init__(self, template_name):
        self.template = template_name

    def get(self):
        return render_template(self.template)

    def post(self):
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(
            login=login,
        ).first()
        if User.check_password(user, password):
            session['auth'] = True
            session['user'] = user
        return redirect('/')


class Logout(MethodView):
    def get(self):
        if session.get('auth'):
            session.pop('auth')
            return redirect('/')


bp.add_url_rule(
    '/logout/',
    view_func=Logout.as_view(
        name='logout',
    ),
)

bp.add_url_rule(
    '/registration/',
    view_func=Registration.as_view(
        name='registration',
        template_name='register_form.jinja2',
    ),
)
bp.add_url_rule(
    '/login/',
    view_func=Login.as_view(
        name='login',
        template_name='login.jinja2',
    ),
)
