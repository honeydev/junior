
# Настройки бекэндов OAuth-авторизации
# Полный список параметров в https://docs.authlib.org/en/latest/client/flask.html#configuration
oauth_backend = {
    'github': {
        'name': 'github',
        'access_token_url': 'https://github.com/login/oauth/access_token',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'api_base_url': 'https://api.github.com/',
        'client_kwargs': {'scope': 'user:email'},
    },
    'yandex': {
        'name': 'yandex',
        'access_token_url': 'https://oauth.yandex.ru/token',
        'authorize_url': 'https://oauth.yandex.ru/authorize',
        'api_base_url': 'https://login.yandex.ru/',
        'token_endpoint_auth_method': 'client_secret_post',
    },
}

# Словарь для приведения профилей с OAuth к модели User
# Полный набор полей в настоящее время: id, login, email, firstname, middlename, lastname

oauth_profile = {
    'github': {
        'get_profile': '/user',
        'profile': {
            'id': 'id',
            'login': 'login',
            'email': 'email',
            'firstname': 'name',
        },
    },
    'yandex': {
        'get_profile': '/info',
        'profile': {
            'id': 'id',
            'login': 'login',
            'email': 'default_email',
            'firstname': 'first_name',
            'lastname': 'last_name',
        },
    },
}
