from wtforms import Form, PasswordField, StringField, validators


class LoginForm(Form):
    login = StringField('Логин', [
        validators.input_required(
            message='Поле логин обязательно для заполнения.',
        ),
        validators.length(
            min=3,
            max=15,
            message='Длина логина от %(min)d до %(max)d символов.',
        ),
    ])
    password = PasswordField('Пароль', [
        validators.data_required(message='Поле обязательно для заполнения.'),
        validators.length(
            min=6,
            max=15,
            message='Длина пароля от %(min)d до %(max)d символов.',
        ),
    ])


class RegistrationForm(Form):
    login = StringField('Логин', [
        validators.input_required(message='Поле обязательно для заполнения.'),
        validators.length(
            min=3,
            max=15,
            message='Длина логина от %(min)d до %(max)d символов.',
        ),
    ])
    password = PasswordField('Пароль', [
        validators.data_required(),
        validators.length(
            min=6,
            max=15,
            message='Длина пароля от %(min)d до %(max)d символов.',
        ),
    ])
    password_confirmation = PasswordField('Подтверждение пароля', [
        validators.data_required(message='Поле обязательно для заполнения.'),
        validators.equal_to('password', message='Пароли должны совпадать.'),
    ])
    email = StringField('Email адрес', [
        validators.email(message='Значение не является почтовым адресом.'),
        validators.data_required(message='Поле обязательно.'),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
    lastname = StringField('Фамилия', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
    firstname = StringField('Имя', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
    middlename = StringField('Отчество', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])


class ProfileForm(Form):
    email = StringField('Email адрес', [
        validators.email(message='Значение не является почтовым адресом.'),
        validators.data_required(message='Поле обязательно.'),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
    lastname = StringField('Фамилия', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
    firstname = StringField('Имя', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
    middlename = StringField('Отчество', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
            message='Длина поля от %(min)d до %(max)d символов.',
        ),
    ])
