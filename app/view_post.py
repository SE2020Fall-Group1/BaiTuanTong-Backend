from flask import Blueprint
from app.models import Like, Comment
from exts import db
from decorators import id_mapping
view_post = Blueprint('view_post', __name__, url_prefix='/post/view')


@view_post.route('/', methods=['GET'])
@id_mapping(['user', 'post'])
def viewPost(user, post, request_form):
    club = post.club
    image_urls = [img.url for img in post.pictures]
    isLiked = post.likes.filter_by(user_id=user.id).one_or_none() is not None
    is_collected = user.collected_posts.filter_by(id=post.id).with_for_update().one_or_none() is not None
    likeCnt = len(post.likes.all())
    comments = [{"content": comment.content,
                 "commenterUsername": comment.commenter.username,
                 "commentTime": comment.publish_time}
                for comment in post.comments]

    return {
        "postId": post.id,
        "publishTime": post.publish_time,
        "title": post.title,
        "content": post.text,
        "imageUrls": image_urls,
        "clubId": club.id,
        "clubName": club.club_name,
        "likeCnt": likeCnt,
        "isLiked": isLiked,
        "isCollected": is_collected,
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
    like = post.likes.filter_by(user_id=user.id).with_for_update().one_or_none()
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


@view_post.route('/collect', methods=['POST'])
@id_mapping(['user', 'post'])
def collect_post(user, post, request_form):
    is_collected = user.collected_posts.filter_by(id=post.id).with_for_update().one_or_none() is not None
    if is_collected:
        user.collected_posts.remove(post)
        db.session.commit()
        return 'collection cancelled', 200
    user.collected_posts.append(post)
    db.session.commit()
    return 'collection added', 200
