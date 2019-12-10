from flask import current_app, flash, session

from src.settings_oauth import oauth_backend, oauth_profile
from src.user.models import User


def get_or_create_user_through_oauth(service: str, profile: dict) -> User:

    # ищем участника в базе по id привязке к сервису oauth
    user: User or None = User.query.filter_by(
        **{f'{service}_id': str(profile['id'])},
    ).first()

    # возвращаем, если находим
    if user is not None:
        return user

    # если не находим и в профиле нет email,
    # то ни создать, ни автоматически привязать не получится, возвращаем пустоту
    if not profile['email']:
        return False

    # если находим, то пытаемся привязать к существующему аккаунту
    user: User or None = User.query.filter_by(
        email=profile['email'],
    ).first()

    # сессия, чтобы в первый раз отправить на страницу профиля
    session['oauth_new'] = True

    if user is not None:
        return link_user_with_oauth(user, service, profile)

    # если не находим, то создаём нового пользователя
    flash(f'Ваш аккаунт был автоматически создан и привязан к {service}.', 'info')
    return User(**{
        'login': profile['login'],
        'email': profile['email'],
        'firstname': profile['firstname'],
        f'{service}_id': profile['id'],
        'image': profile['email'],
        'is_oauth': True,
        'is_aproved': True,
    }).save()


def get_remote_profile(service: str, client) -> dict:
    # Получает удалённый профиль пользователя OAuth.
    profile_setting = oauth_profile[service]
    profile_remote = client.get(profile_setting['get_profile']).json()

    return adapt_remote_profile(service, profile_remote)


def adapt_remote_profile(service: str, profile: dict) -> dict:
    # Приводит полученный профиль к стандартному набору полей.
    # Выделена отдельно для использования в тестах.
    profile_setting = oauth_profile[service]
    profile_dict = {}

    for key, kv in profile_setting['profile'].items():
        profile_dict[key] = profile.get(kv, '')

    return profile_dict


def link_user_with_oauth(user: User, service: str, profile: dict) -> User:

    # ищём совпадение по логину и есть такой уже есть, при этом email разные,
    # то добавляем к новому логину постфикс
    tmp_user = User.query.filter_by(login=profile['login']).first()
    if (tmp_user                                                   # noqa WPS337
            and tmp_user.login == profile['login']
            and tmp_user.email != profile['email']):
        login = '{0}~{1}'.format(profile['login'], service)
    else:
        login = user.login

    User.query.filter_by(email=profile['email']).update({
        'login': login,
        f'{service}_id': profile['id'],
        'is_oauth': True,
        'is_aproved': True,
    })

    flash(f'Ваш аккаунт был привязан к {service} по совпадению email.', 'info')
    flash('Вы можете отвязать его в любой момент из профиля.', 'info')

    return user


def register_oauth_backend(backend: str, oauth) -> None:
    # Обёртка для регистрации бекэндов при запуске приложения
    return oauth.register(**oauth_backend[backend])


def update_is_oauth(user) -> None:
    # Отключает поле is_oauth, если все сервисы авторизации отключены
    # Используется при удалении ссылки на любой из них (DelinkOAuth)
    user_oauth = user.get_oauth_dict()

    is_oauth = False
    for backend in current_app.config['OAUTH_BACKEND']:
        if user_oauth.get(backend, False):
            is_oauth = True

    User.query.filter_by(id=user.id).update({'is_oauth': is_oauth})
