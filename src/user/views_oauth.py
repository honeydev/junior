from flask import (current_app, flash, redirect, render_template, request,
                   session, url_for)
from flask.views import MethodView
from flask_dance.contrib.github import github
from werkzeug.datastructures import MultiDict

from src.user.forms import ProfileOAuthForm
from src.user.models import User
from src.views import BaseView


class DeLinkOAuth(MethodView):
    """Обрабатывает отвязку от OAuth."""

    def get(self):
        user = session['auth'].user
        # разрешаем отвязывать только при наличии пароля, иначе нельзя будет войти
        if user.password:
            User.query.filter_by(login=user.login).update({
                'github_id': '',
                'is_oauth': False,
                'is_aproved': True,
            })
            try:
                del current_app.blueprints['github'].token # noqa WPS420
            except KeyError:
                pass # noqa WPS420 (при авторизации через сайт, токена гитхаба нет)
            return redirect(url_for('auth.profile'))

        flash('Для отвязки аккаунта у вас должен быть установлен пароль.', 'error')
        return redirect(url_for('auth.profile_oauth'))


class LinkOAuth(MethodView):
    """Обрабатывает привязку к OAuth."""

    def get(self):
        session['oauth_link'] = True
        return redirect(url_for('github.login'))


class LoginOAuth(MethodView):
    """
    Обрабатывает вход через OAuth.

    Если регистрация не заверешена, то на форму профиля, иначе на заглавную страницу
    Тут же обрабатываем привязку к существующему аккаунту по кнопке с профиля

    oauth_link - задаётся в LinkOAuth(), даёт понять, что будет привязка
    """

    def get(self):
        user = session['auth'].user
        if github.authorized:
            if session.get('oauth_link', False):
                github_id = github.get('user').json().get('id')
                if User.query.filter_by(github_id=str(github_id)).first():
                    flash(
                        'Данный аккаунт GitHub уже привязан к другому аккаунту на данном сайте.',
                        'error',
                    )
                    return redirect(url_for('auth.profile'))
                User.query.filter_by(login=user.login).update({
                    'github_id': github_id,
                    'is_oauth': True,
                    'is_aproved': True,
                })
                session['oauth_link'] = False
                return redirect(url_for('auth.profile_oauth'))
            if not user.is_oauth:
                return redirect(url_for('auth.profile_oauth'))
        return redirect(url_for('index.home'))


class ProfileOAuth(BaseView):
    """Профиль участников, у кого подключён OAuth."""

    def __init__(self, template_name):
        super().__init__(template_name)
        self.form = ProfileOAuthForm
        self.user = session['auth'].user

    def post(self):
        form = self.form(request.form)
        if not form.validate():
            return render_template(self.template_name, **self.context)
        login = request.form.get('login')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        user_data = {
            'login': login,
            'email': email,
            'firstname': firstname,
            'middlename': middlename,
            'lastname': lastname,
            'image': email,
            'is_oauth': True,
        }
        # отдельно смотрим пароль:
        #   если стоит флаг, то меняем
        #   если пароль пустой, то сбрасываем
        if request.form.get('change_password'):
            password = request.form.get('password') if request.form.get('password') else False
            pass_hash = User.hash_password(password).decode() if password else ''
            user_data['password'] = pass_hash

        if login != self.user.login:
            if User.query.filter_by(login=login).first():
                flash('Логин уже занят.', 'error')
                return render_template(
                    self.template_name,
                    **{'form': form},
                )

        if email != self.user.email:
            if User.query.filter_by(email=email).first():
                flash('Такой e-mail уже привязан к другому аккаунту.', 'error')
                return render_template(
                    self.template_name,
                    **{'form': form},
                )

        User.query.filter_by(github_id=self.user.github_id).update(user_data)
        return redirect(url_for('auth.profile_oauth'))

    def get(self):
        if self.user.is_oauth or github.authorized:
            user_data = MultiDict([
                ('login', self.user.login),
                ('email', self.user.email),
                ('change_password', False),
                ('firstname', self.user.firstname),
                ('middlename', self.user.middlename),
                ('lastname', self.user.lastname),
            ])
            self.context['form'] = self.form(user_data)
            return render_template(self.template_name, **self.context)

        return redirect(url_for('index.home'))
