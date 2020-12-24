from flask import Blueprint
from .models import Post, Club
from exts import db
from decorators import id_mapping

manage_post = Blueprint('manage_post', __name__, url_prefix='/post')


@manage_post.route('/release', methods=['POST'])
@id_mapping(['club'])
def release_post(club, request_form):
    title = request_form.get('title')
    text = request_form.get('text')
    post = Post(title=title, text=text, club_id=club.id)
    try:
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200


@manage_post.route('/delete', methods=['POST'])
@id_mapping(['post'])
def delete_post(post, request_form):
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200


@manage_post.route('/edit', methods=['POST'])
@id_mapping(['post'])
def edit_post(post, request_form):
    title = request_form.get('title')
    text = request_form.get('text')
    try:
        post.title = title
        post.text = text
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200

