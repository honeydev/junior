from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask.views import MethodView
from werkzeug.datastructures import MultiDict

from src.mailers.send_mail import send_mail_for_aprove
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
        image = request.form.get('email')
        pass_hash = User.hash_password(password)
        user = User(
            login=login,
            email=email,
            password=pass_hash.decode(),
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            image=image,
        )
        if User.query.filter_by(login=login).first():
            return render_template(
                self.template,
                **{'form': form, 'info': 'Логин уже занят'},
            )
        if User.query.filter_by(email=email).first():
            return render_template(
                self.template,
                **{'form': form, 'info': 'Email уже занят'},
            )
        User.save(user)
        if send_mail_for_aprove(user):
            flash('Вам на почту отправлена ссылка для подтверждения регистрации')
        else:
            flash('Сбой отправки письма')
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
            if not user.is_aproved:
                flash('Завершите регистрацию, пройдя по ссылке, отправленной на почту')
                return redirect(url_for('auth.login'))
            session['auth'] = SessionAuth(True, user)
        return redirect('/')


class Profile(BaseView):
    def __init__(self, template_name):
        super().__init__(template_name)
        self.user = session['auth'].user
        self.form = ProfileForm

    def get(self):
        user_data = MultiDict([
            ('email', self.user.email),
            ('firstname', self.user.firstname),
            ('middlename', self.user.middlename),
            ('lastname', self.user.lastname),
        ])
        self.context['form'] = self.form(user_data)
        return render_template(self.template_name, **self.context)

    def post(self):
        form = self.form(request.form)
        if not form.validate():
            return render_template(self.template, **{'form': form})
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


class EmailAprove(MethodView):
    """Функция проверки ссылки.

    по ней переходит пользователь, завершая регистрацию
    """

    def get(self, token):
        user = User.verify_token_for_mail_aproved(token)
        if not user:
            return redirect(url_for('index.index'))
        return redirect(url_for('auth.login'))


class ChangeAvatar(BaseView):
    def __init__(self, template_name):
        super().__init__(template_name)
        self.user = session['auth'].user
        self.form = ChangeAvatarForm

    def get(self):
        self.context['form'] = self.form()
        return render_template(self.template_name, **self.context)

    def post(self):
        return redirect(url_for('auth.change_avatar'))


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

bp.add_url_rule(
    '/email_aprove/<token>',
    view_func=EmailAprove.as_view(
        name='email_aprove',
    ),
)
bp.add_url_rule(
    '/change_avatar/',
    view_func=ChangeAvatar.as_view(
        name='change_avatar',
        template_name='change_avatar.jinja2',
    ),
)
