from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask.views import MethodView
from werkzeug.datastructures import MultiDict

from src.user.auth import SessionAuth
from src.user.forms import LoginForm, ProfileForm, RegistrationForm
from src.user.models import User
from src.views import BaseView

bp = Blueprint('auth', __name__, template_folder='templates')


class Registration(MethodView):

    def __init__(self, template_name):
        self.template: str = template_name
        self.form = RegistrationForm

    def post(self):
        form = self.form(request.form)
        if not form.validate():
            return render_template(self.template, **{'form': form})
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
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
            return render_template(
                self.template,
                **{'form': form, 'info': 'Логин уже занят'},
            )

        User.save(user)
        return redirect(url_for('auth.login'))

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

        if user and User.check_password(user, password):
            session['auth'] = SessionAuth(True, user)
            return redirect(url_for('index.index'))

        return render_template(self.template, error=True, **{'form': form})


class Profile(BaseView):
    def __init__(self, template_name):
        super().__init__(template_name)
        self.form = ProfileForm

    def get(self):
        user = User.query.filter_by(login=session['auth'].user.login).first()
        user_data = MultiDict([
            ('email', user.email),
            ('firstname', user.firstname),
            ('middlename', user.middlename),
            ('lastname', user.lastname),
        ])
        self.context['form'] = self.form(user_data)
        return render_template(self.template_name, **self.context)

    def post(self):
        form = self.form(request.form)
        if not form.validate():
            return render_template(self.template_name, **{'form': form}, **self.context)
        User.query.filter_by(login=session['auth'].user.login).update({
            'email': request.form.get('email'),
            'firstname': request.form.get('firstname'),
            'middlename': request.form.get('middlename'),
            'lastname': request.form.get('lastname'),
        })
        return redirect(url_for('auth.profile'))


class Logout(MethodView):
    def get(self):
        auth = session.get('auth')
        auth.logout()
        return redirect(url_for('index.index'))


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
bp.add_url_rule(
    '/profile/',
    view_func=Profile.as_view(
        name='profile',
        template_name='profile_form.jinja2',
    ),
)
