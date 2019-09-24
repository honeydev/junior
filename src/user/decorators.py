from functools import wraps

from flask import abort, session


def login_required_user(f):
    """Login required decorator, add user obj in func."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = session.get('auth', False)
        user = session.get('user', None)
        if not auth or not user:
            abort(401)
        return f(user, *args, **kwargs)
    return decorated_function


def login_required(f):
    """Login required decorator, without user obj."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = session.get('auth', False)
        if not auth:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
