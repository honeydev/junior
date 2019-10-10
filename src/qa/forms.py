from wtforms import Form

from src.admin_forms import CKTextAreaField


class AnswerForm(Form):
    text = CKTextAreaField()
