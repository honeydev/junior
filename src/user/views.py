from flask import Blueprint, redirect, render_template, request, session
from flask.views import MethodView

from src.user.forms import LoginForm, RegistrationForm
from src.user.models import User

bp = Blueprint('auth', __name__, template_folder='templates')


class Registration(MethodView):

    def __init__(self, template_name):
        self.template: str = template_name
        self.form = RegistrationForm

    def post(self):
        form = self.form(request.form)
        if not form.validate():
            return render_template(self.template, **{'form': form})
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
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
        if User.query.filter_by(login=login).first():
            result = render_template(
                self.template,
                **{'form': form, 'info': 'Логин уже занят'}
            )
        else:
            User.save(user)
            result = redirect('/login')
        return result

    def get(self):
        return render_template(self.template, **{'form': self.form()})


class Login(MethodView):
    def __init__(self, template_name):
        self.template = template_name
        self.form = LoginForm

    def get(self):
        return render_template(self.template, **{'form': self.form()})

    def post(self):
        form = self.form(request.form)

        if not form.validate():
            return render_template(self.template, **{'form': form})

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
