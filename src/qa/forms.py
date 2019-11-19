from wtforms import Form, validators

from src.admin_forms import CKTextAreaField


class AnswerForm(Form):
    text = CKTextAreaField('Ответ', [
        validators.InputRequired(message='Ответ не может быть пустым.'),
        validators.Length(max=600, message='Ответ слишком длинный.'),  # noqa: WPS432
    ])
