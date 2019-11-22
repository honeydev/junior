from wtforms import BooleanField, Form, PasswordField, StringField, validators


class BaseForm(Form):
    class Meta:
        locales = ['ru']


class LoginForm(BaseForm):
    login = StringField('Логин', [
        validators.input_required(),
        validators.length(
            min=3,
            max=15,
        ),
    ])
    password = PasswordField('Пароль', [
        validators.data_required(),
        validators.length(
            min=6,
            max=15,
        ),
    ])


class RegistrationForm(BaseForm):
    login = StringField('Логин', [
        validators.input_required(),
        validators.length(
            min=3,
            max=15,
        ),
    ])
    password = PasswordField('Пароль', [
        validators.data_required(),
        validators.length(
            min=6,
            max=15,
        ),
    ])
    password_confirmation = PasswordField('Подтверждение пароля', [
        validators.data_required(),
        validators.equal_to('password', message='Пароли должны совпадать.'),
    ])
    email = StringField('Email адрес', [
        validators.email(),
        validators.data_required(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    lastname = StringField('Фамилия', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    firstname = StringField('Имя', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    middlename = StringField('Отчество', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])


class ProfileOAuthForm(BaseForm):
    login = StringField('Логин', [
        validators.input_required(),
        validators.length(
            min=3,
            max=15,
        ),
    ])
    change_password = BooleanField('Сменить/установить пароль')
    password = PasswordField('Пароль', [
        validators.optional(),
        validators.length(
            min=6,
            max=15,
        ),
        validators.equal_to('password', message='Пароли должны совпадать.'),
    ])
    password_confirmation = PasswordField('Подтверждение пароля')
    email = StringField('Email адрес', [
        validators.email(),
        validators.data_required(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    lastname = StringField('Фамилия', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    firstname = StringField('Имя', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    middlename = StringField('Отчество', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])


class ProfileForm(BaseForm):
    email = StringField('Email адрес', [
        validators.email(),
        validators.data_required(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    lastname = StringField('Фамилия', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    firstname = StringField('Имя', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
    middlename = StringField('Отчество', [
        validators.optional(),
        validators.length(
            min=4,
            max=30,
        ),
    ])
