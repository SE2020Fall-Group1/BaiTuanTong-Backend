import json
from flask import Blueprint, request
from decorators import login_required
from app.models import Post
from exts import db

manage_post = Blueprint('manage_post', __name__, url_prefix='/post')


@manage_post.route('/release', methods=['POST'])
@login_required
def release_post():
    request_form = json.loads(request.get_data(as_text=True))
    title = request_form.get('title')
    text = request_form.get('text')
    post = Post(title=title, text=text)
    try:
        db.session.add(post)
        db.session.commit()
    except Exception:
        return 'release failed', 500
    return 'success', 200


@manage_post.route('/delete', methods=['POST'])
@login_required
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
@login_required
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
