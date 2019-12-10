from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask.views import MethodView
from werkzeug.datastructures import MultiDict

from src.extensions import db
from src.mailers.send_mail import send_mail_for_aprove
from src.user.auth import SessionAuth
from src.user.decorators import login_required
from src.user.forms import (ChangeAvatarForm, LoginForm, ProfileForm,
                            ProfileOAuthForm, RegistrationForm,
                            ResendEmailForm)
from src.user.models import User
from src.views import BaseView

bp = Blueprint('auth', __name__, template_folder='templates')


class Registration(MethodView):

    def __init__(self, template_name):
        self.template: str = template_name
        self.form = RegistrationForm
        self.context = {'oauth_backend': current_app.config['OAUTH_BACKEND']}

    def post(self):
        self.context['form'] = form = self.form(request.form)  # noqa: WPS204

        if not form.validate():
            return render_template(self.template, **self.context)  # noqa: WPS204

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
            gravatar='gravatar',
        )
        if User.query.filter_by(login=login).first():
            flash('Логин уже занят.', 'error')
            return render_template(
                self.template,
                **self.context,
            )
        if User.query.filter_by(email=email).first():
            flash('Такой e-mail уже привязан к другому аккаунту.', 'error')
            return render_template(
                self.template,
                **self.context,
            )
        User.save(user)
        if send_mail_for_aprove(user):
            flash('Вам на почту отправлена ссылка для подтверждения регистрации', 'info')
        else:
            flash('Сбой отправки письма', 'error')
        return redirect(url_for('auth.login'))

    def get(self):
        self.context['form'] = self.form()
        return render_template(self.template, **self.context)


class Login(MethodView):
    def __init__(self, template_name):
        self.template = template_name
        self.form = LoginForm
        self.context = {'oauth_backend': current_app.config['OAUTH_BACKEND']}

    def get(self):
        self.context['form'] = self.form()
        return render_template(self.template, **self.context)

    def post(self):
        self.context['form'] = form = self.form(request.form)

        if not form.validate():
            return render_template(self.template, **self.context)

        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(
            login=login,
        ).first()

        if user and User.check_password(user, password):
            if not user.is_aproved:
                flash('Завершите регистрацию, пройдя по ссылке, отправленной на почту', 'error')
                return redirect(url_for('auth.login'))
            session['auth'] = SessionAuth(True, user)
            if request.referrer and 'answer' in request.referrer:
                return redirect(request.referrer)
            return redirect(url_for('index.home'))
        flash('Неверный логин или пароль!', 'error')
        return render_template(self.template, **self.context)


class Profile(BaseView):
    def __init__(self, template_name):
        super().__init__(template_name)
        self.user = session['auth'].user
        self.form = ProfileForm

    def get(self):
        if self.user.is_oauth:
            return redirect(url_for('auth.profile_oauth'))
        user_data = MultiDict([
            ('email', self.user.email),
            ('firstname', self.user.firstname),
            ('middlename', self.user.middlename),
            ('lastname', self.user.lastname),
        ])
        self.context['form'] = self.form(user_data)
        return render_template(self.template_name, **self.context)

    def post(self):
        self.context['form'] = form = self.form(request.form)
        if not form.validate():
            return render_template(self.template, **self.context)
        User.query.filter_by(login=session['auth'].user.login).update({
            'email': request.form.get('email'),
            'firstname': request.form.get('firstname'),
            'middlename': request.form.get('middlename'),
            'lastname': request.form.get('lastname'),
        })
        return redirect(url_for('auth.profile'))


class ProfileOAuth(BaseView):
    """Профиль участников, у кого подключён OAuth."""

    def __init__(self, template_name):
        super().__init__(template_name)
        self.form = ProfileOAuthForm
        self.user = session['auth'].user

    def post(self):
        self.context['form'] = form = self.form(request.form)
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
                    **self.context,
                )

        if email != self.user.email:
            if User.query.filter_by(email=email).first():
                flash('Такой e-mail уже привязан к другому аккаунту.', 'error')
                return render_template(
                    self.template_name,
                    **self.context,
                )

        User.query.filter_by(github_id=self.user.github_id).update(user_data)
        return redirect(url_for('.profile_oauth'))

    def get(self):
        if self.user.is_oauth:
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


class Logout(MethodView):
    def get(self):
        auth = session.get('auth')
        auth.logout()
        return redirect(url_for('index.home'))


class EmailAprove(MethodView):
    """Функция проверки ссылки.

    по ней переходит пользователь, завершая регистрацию
    """

    def get(self, token):
        user = User.verify_token_for_mail_aproved(token)
        if not user:
            return redirect(url_for('index.home'))
        return redirect(url_for('auth.login'))


class EmailResend(MethodView):
    """Resend email function."""

    def __init__(self, template_name):
        self.template: str = template_name
        self.form = ResendEmailForm

    def post(self):
        form = self.form(request.form)
        if not form.validate():
            return render_template(self.template, **{'form': form})
        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()
        if user:
            if send_mail_for_aprove(user):
                flash('Вам на почту отправлена ссылка для подтверждения регистрации', 'info')
            else:
                flash('Сбой отправки письма', 'error')
        else:
            flash('Пользователь с таким email не зарегистрирован', 'error')
        return redirect(url_for('auth.login'))

    def get(self):
        return render_template(self.template, **{'form': self.form()})


class ChangeAvatar(BaseView):
    def __init__(self, template_name):
        super().__init__(template_name)
        self.user = session['auth'].user
        self.form = ChangeAvatarForm

    def get(self):
        if self.user.gravatar:
            avatar_type = 'gravatar'
        else:
            avatar_type = 'face'

        user_data = MultiDict([
            ('chosen_avatar', avatar_type),
            ('avatar_img_str', self.user.image),
        ])
        self.context['form'] = self.form(user_data)
        return render_template(self.template_name, **self.context)

    def post(self):
        # выбор типа аватарки - граватар или рожица
        avatar_type = request.form.get('chosen_avatar')
        new_img = self.user.image
        if request.form.get('avatar_img_str'):
            new_img = request.form.get('avatar_img_str')

        # если аватар по умолчанию -
        # подтягивается граватар по email пользователя
        if request.form.get('default_avatar'):
            avatar_type = 'gravatar'
            new_img = self.user.email
        User.query.filter_by(login=session['auth'].user.login).update({
            'image': new_img,
            'gravatar': avatar_type,
        })
        db.session.commit()

        return redirect(url_for('auth.change_avatar'))


bp.add_url_rule(
    '/logout/',
    view_func=login_required(Logout.as_view(
        name='logout',
    )),
)

bp.add_url_rule(
    '/registration/',
    view_func=Registration.as_view(
        name='registration',
        template_name='user/register_form.jinja2',
    ),
)

bp.add_url_rule(
    '/login/',
    view_func=Login.as_view(
        name='login',
        template_name='user/login.jinja2',
    ),
)

bp.add_url_rule(
    '/profile/',
    view_func=login_required(Profile.as_view(
        name='profile',
        template_name='user/profile_form.jinja2',
    )),
)

bp.add_url_rule(
    '/profile_oauth/',
    view_func=login_required(ProfileOAuth.as_view(
        name='profile_oauth',
        template_name='user/profile_oauth_form.jinja2',
    )),
)

bp.add_url_rule(
    '/email_aprove/<token>',
    view_func=EmailAprove.as_view(
        name='email_aprove',
    ),
)

bp.add_url_rule(
    '/resend_email/',
    view_func=EmailResend.as_view(
        name='resend_email',
        template_name='user/resend_email_form.jinja2',
    ),
)

bp.add_url_rule(
    '/change_avatar/',
    view_func=ChangeAvatar.as_view(
        name='change_avatar',
        template_name='user/change_avatar.jinja2',
    ),
)
