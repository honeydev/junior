from functools import wraps
from http import HTTPStatus

from flask import abort, session

from src.user.models import User


def login_required_user(wrapped_callable):
    """Login required decorator, add user obj in func."""
    @wraps(wrapped_callable)
    def decorated_function(*args, **kwargs):
        auth = session.get('auth', False)
        if not auth:
            abort(int(HTTPStatus.UNAUTHORIZED))
        return wrapped_callable(*args, user=User.query.get(auth.user.id), **kwargs)
    return decorated_function


def login_required(wrapped_callable):
    """Login required decorator, without user obj."""
    @wraps(wrapped_callable)
    def decorated_function(*args, **kwargs):
        auth = session.get('auth', False)
        if not auth:
            abort(int(HTTPStatus.UNAUTHORIZED))
        return wrapped_callable(*args, **kwargs)
    return decorated_function
