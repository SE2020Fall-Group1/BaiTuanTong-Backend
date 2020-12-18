from flask import Blueprint
from app.models import Like, Comment
from exts import db
from decorators import id_mapping
view_post = Blueprint('view_post', __name__, url_prefix='/post/view')


@view_post.route('/', methods=['GET'])
@id_mapping(['user', 'post'])
def viewPost(user, post, request_form):
    club = post.club
    isLiked = post.likes.filter_by(user_id=user.id).one_or_none() is not None
    likeCnt = len(post.likes.all())
    comments = [{"content": comment.content, "commenterUsername": comment.commenter.username}
                for comment in post.comments]

    return {
        "postId": post.id,
        "publishTime": post.publish_time,
        "title": post.title,
        "content": post.text,
        "clubId": club.id,
        "clubName": club.club_name,
        "likeCnt": likeCnt,
        "isLiked": isLiked,
        "comments": comments,
    }


@view_post.route('/info', methods=['GET'])
@id_mapping(['user', 'post'])
def viewPostInfo(user, post, request_form):
    isLiked = post.likes.filter_by(user_id=user.id).one_or_none() is not None
    likeCnt = len(post.likes.all())
    commentCnt = len(post.comments.all())

    return {
        "isLiked": isLiked,
        "likeCnt": likeCnt,
        "commentCnt": commentCnt
    }


@view_post.route('/like', methods=['POST'])
@id_mapping(['user', 'post'])
def alter_like(user, post, request_form):
    post.likes.with_for_update()
    like = post.likes.filter_by(user_id=user.id).one_or_none()
    if like:
        db.session.delete(like)
        db.session.commit()
        return 'success', 200
    like = Like(user_id=user.id, post_id=post.id)
    try:
        db.session.add(like)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200


@view_post.route('/comment', methods=['POST'])
@id_mapping(['user', 'post'])
def release_comment(user, post, request_form):
    comment_text = request_form.get('commentText')
    comment = Comment(user_id=user.id, post_id=post.id, content=comment_text)
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200
