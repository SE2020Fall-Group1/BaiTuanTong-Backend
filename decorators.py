from functools import wraps
from flask import session


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        return "not login error", 401
    return wrapper
