import json
from flask import Blueprint, request
from .models import Post, Club
from exts import db

manage_post = Blueprint('manage_post', __name__, url_prefix='/post')


@manage_post.route('/release', methods=['POST'])
def release_post():
    request_form = json.loads(request.get_data(as_text=True))
    club_id = request_form.get('clubId')
    title = request_form.get('title')
    text = request_form.get('text')
    club = Club.query.filter_by(id=club_id).one_or_none()
    if not club:
        return 'invalid clubId', 400
    post = Post(title=title, text=text, club_id=club_id)
    try:
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200


@manage_post.route('/delete', methods=['POST'])
def delete_post():
    request_form = json.loads(request.get_data(as_text=True))
    post_id = request_form.get('postId')
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return "invalid postId", 400
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception:
        return 'delete failed', 500
    return 'success', 200


@manage_post.route('/edit', methods=['POST'])
def edit_post():
    request_form = json.loads(request.get_data(as_text=True))
    post_id = request_form.get('postId')
    text = request_form.get('text')
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return "invalid postId", 400
    try:
        post.text = text
        db.session.commit()
    except Exception:
        return 'edit failed', 500
    return 'success', 200
