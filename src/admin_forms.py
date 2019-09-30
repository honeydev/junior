from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'  # noqa WPS336
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)  # noqa WPS608


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class QuestionWYSIWYG(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'text': CKTextAreaField,
    }
