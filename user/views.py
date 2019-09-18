from flask.views import MethodView
from flask import Blueprint

bp = Blueprint('auth', __name__)


class Registration(MethodView):

    def post(self):
        """Регистрация."""
        pass

    def get(self):
        """Форма регистрации."""
        pass

    def dispatch_request(self, *args, **kwargs):
        pass


bp.add_url_rule('/auth/', view_func=Registration.as_view(name='auth'))
