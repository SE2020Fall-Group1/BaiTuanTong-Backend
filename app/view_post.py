import json
from flask import Blueprint, request, jsonify
from .models import Post, Like, User
from .utils import is_valid_user_id
from exts import db
from decorators import id_mapping


view_post = Blueprint('view_post', __name__, url_prefix='/post/view')


@view_post.route('/', methods=['GET'])
@id_mapping(['user', 'post'])
def viewPost(user, post):
    clubName = post.club.club_name
    isLiked = post.likes.filter_by(id=user.id).one_or_none() is not None
    likeCnt = len(post.likes.all())
    comments = [{"content": comment.content, "commenterUsername": comment.commenter.username}
                for comment in post.comments]

    return {
        "postId": post.id,
        "publishTime": post.publish_time,
        "title": post.title,
        "content": post.text,
        "clubName": clubName,
        "likeCnt": likeCnt,
        "isLiked": isLiked,
        "comments": comments
    }


@view_post.route('/like', methods=['POST'])
@id_mapping(['user', 'post'])
def alter_like(user, post):
    like = post.likes.filter_by(user_id=user.id).one_or_none()
    if like:
        db.session.delete(like)
        db.session.commit()
        return 'success', 200
    like = Like(user_id=user.id, post_id=post.id)
    db.session.add(like)
    db.commit()
    return 'success', 200
