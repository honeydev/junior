from wtforms import Form, PasswordField, StringField, validators


class LoginForm(Form):
    login = StringField('Логин', [
        validators.input_required(
            message='Поле логин обязательно для заполнения.'
        ),
        validators.length(
            min=3, max=15, message='Длинна логина от 3 до 15 символов.'
        )
    ])
    password = PasswordField('Пароль', [
        validators.data_required(message='Поле обязательно для заполнения.'),
        validators.length(
            min=3, max=15, message='Длинна пароля от 6 до 15 символов.'
        )
    ])


class RegistrationForm(Form):
    login = StringField('Логин', [
        validators.input_required(message='Поле обязательно для заполнения.'),
        validators.length(
            min=3, max=15, message='Длинна логина от 3 до 15 символов.'
        )
    ])
    password = PasswordField('Пароль', [
        validators.data_required(),
        validators.length(
            min=6, max=15, message='Длинна пароля от 6 до 15 символов.'
        )
    ])
    password_confirmation = PasswordField('Подтверждение пароля', [
        validators.data_required(message='Поле обязательно для заполнения.'),
        validators.length(
            min=6, max=15, message='Длинна пароля от 6 до 15 символов.'
        ),
        validators.equal_to('password', message='Пароли должны совпадать.')
    ])
    email = StringField('Email адрес', [
        validators.email(message='Значение не является почтовый адресом.'),
        validators.data_required(message='Поле обязательно.'),
        validators.length(
            min=4, max=30, message='Длинна поля от 4 до 30 символов.'
        )
    ])
    middlename = StringField('Фамилия', [
        validators.optional(),
        validators.length(
            min=4, max=30, message='Длинна поля от 4 до 30 символов.'
        )
    ])
    firstname = StringField('Имя', [
        validators.optional(),
        validators.length(
            min=4, max=30, message='Длинна поля от 4 до 30 символов.'
        )
    ])
    lastname = StringField('Отчество', [
        validators.optional(),
        validators.length(
            min=4, max=30, message='Длинна поля от 4 до 30 символов.'
        )
    ])
