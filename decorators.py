import json
from functools import wraps
from flask import session, request
from app.models import User, Club, Post


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        return "not login error", 401
    return wrapper


def id_mapping(id_types):
    def validation(func):
        @wraps(func)
        def wrapper():
            request_form = json.loads(request.get_data(as_text=True)) if request.method == 'POST' else request.args
            param = {}
            if 'user' in id_types:
                user_id = request_form.get('userId')
                user = User.query.filter_by(id=user_id).one_or_none()
                if not user:
                    return 'invalid userId', 400
                param['user'] = user
            if 'club' in id_types:
                club_id = request_form.get('clubId')
                club = Club.query.filter_by(id=club_id).one_or_none()
                if not club:
                    return 'invalid clubId', 400
                param['club'] = club
            if 'post' in id_types:
                post_id = request_form.get('postId')
                post = Post.query.filter_by(id=post_id).one_or_none()
                if not post:
                    return 'invalid postId', 400
                param['post'] = post
            return func(**param)
        return wrapper
    return validation
