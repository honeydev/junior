from flask import Blueprint, flash, redirect, session, url_for
from flask.views import MethodView

from src.extensions import oauth
from src.user.auth import SessionAuth
from src.user.decorators import login_required
from src.user.models import User
from src.user.oauth import get_remote_profile, update_is_oauth

bp: Blueprint = Blueprint('oauth', __name__)


class AuthorizedOAuth(MethodView):
    """Callback после авторизации в OAuth-сервисе.

    session:
        oauth_link - задаётся в LinkOAuth(), даёт понять, что будет привязка
        new_oauth - задаётся в get_or_create_user_through_oauth()
        даёт понять, что свежая привязка и первый раз показывает страницу профиля
    """

    def get(self, service):
        client = oauth.create_client(service)

        if client.authorize_access_token():
            profile = get_remote_profile(service, client)
            if session.get('oauth_link', False):
                user = session['auth'].user
                service_name = f'{service}_id'
                service_id = profile['id']
                if User.query.filter_by(**{service_name: str(service_id)}).first():
                    flash(
                        f'Данный аккаунт {service} уже привязан '
                        + 'к другому аккаунту на данном сайте.',
                        'error',
                    )
                    return redirect(url_for('auth.profile'))

                User.query.filter_by(id=user.id).update({
                    service_name: service_id,
                    'is_oauth': True,
                    'is_aproved': True,
                })

                session['oauth_link'] = False
                flash(f'Ваш аккаунт был привязан к {service}.', 'info')
                return redirect(url_for('auth.profile_oauth'))
            else:
                session['auth'] = SessionAuth.create_from_oauth(service, profile)
                if session.get('oauth_new', False):
                    return redirect(url_for('auth.profile_oauth'))

        return redirect(url_for('index.home'))


class DeLinkOAuth(MethodView):
    """Обрабатывает отвязку от OAuth."""

    def get(self, service):
        user = session['auth'].user

        # разрешаем отвязывать только при наличии пароля или других привязок
        # иначе нельзя будет войти на сайт с пустым паролем
        oauth_list = filter(lambda x: x is not None, user.get_oauth_dict().values())  # noqa: WPS111
        if user.password or len(list(oauth_list)) > 1:
            User.query.filter_by(login=user.login).update({
                f'{service}_id': '',
            })

            update_is_oauth(user)
            session['auth'].logout()
            session['auth'] = SessionAuth(True, user)

            flash(f'Ваш аккаунт был отвязан от {service}.', 'info')
            return redirect(url_for('auth.profile'))

        flash(
            'Для отвязки аккаунта у вас должен быть установлен пароль.<br>'
            + 'Или привяжите другой OAuth-сервис к аккаунту.',
            'error',
        )
        return redirect(url_for('auth.profile_oauth'))


class LinkOAuth(MethodView):
    """Обрабатывает привязку к OAuth."""

    def get(self, service):
        session['oauth_link'] = service
        return redirect(url_for('.login', **{'service': service}))


class LoginOAuth(MethodView):
    """Перенапрявляет на OAuth-сервис."""

    def get(self, service):
        client = oauth.create_client(service)
        return client.authorize_redirect(url_for(
            '.authorized',
            _external=True,
            **{'service': service},
        ))


bp.add_url_rule(
    '/oauth/authorized/<service>/',
    view_func=AuthorizedOAuth.as_view(
        name='authorized',
    ),
)

bp.add_url_rule(
    '/oauth/link/<service>/',
    view_func=login_required(LinkOAuth.as_view(
        name='link',
    )),
)

bp.add_url_rule(
    '/oauth/delink/<service>/',
    view_func=login_required(DeLinkOAuth.as_view(
        name='delink',
    )),
)

bp.add_url_rule(
    '/oauth/login/<service>/',
    view_func=LoginOAuth.as_view(
        name='login',
    ),
)
