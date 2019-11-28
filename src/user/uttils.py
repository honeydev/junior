from flask import flash, session

from src.user.models import User


def get_or_create_user_through_oauth(profile: dict, service: str) -> User:

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
    session['new_oauth'] = True

    if user is not None:
        return link_user_with_oauth(user, profile, service)

    # если не находим, то создаём нового пользователя
    flash('Ваш аккаунт был автоматически создан и привязан к {service}.', 'info')
    return User(**{
        'login': profile['login'],
        'email': profile['email'],
        'firstname': profile['name'],
        f'{service}_id': profile['id'],
        'image': profile['email'],
        'is_oauth': True,
        'is_aproved': True,
    }).save()


def link_user_with_oauth(user: User, profile: dict, service: str) -> User:

    # ищём совпадение по логину и есть такой уже есть, при это email разные,
    # то добавляем к новому логину постфикс
    tmp_user = User.query.filter_by(login=profile['login']).first()
    if (tmp_user                                                   # noqa WPS337
            and tmp_user.get('login') == profile['login']
            and tmp_user.get('email') != profile['email']):
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
