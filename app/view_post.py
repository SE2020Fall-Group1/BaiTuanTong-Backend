from flask import Blueprint, request
from .models import Post, Like
from decorators import login_required
view_post = Blueprint('view_post', __name__, url_prefix='/post')


@view_post.route('/view', methods=['GET'])
@login_required
def viewPost():
    user_id = request.args.get('userId')
    post_id = request.args.get('postId')
    print(post_id)
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return "invalid postId"

    clubName = post.club.club_name
    isLiked = Like.query.filter_by(user_id=user_id, post_id=post_id).first() is not None
    likeCnt = len(post.likes)
    comments = [{"content": comment.content, "commenterUsername": comment.commenter.username}
                for comment in post.comments]
    publish_time = post.publish_time

    return {
        "postId": post_id,
        "publishTime": post.publish_time,
        "title": post.title,
        "content": post.text,
        "clubName": clubName,
        "likeCnt": likeCnt,
        "isLiked": isLiked,
        "comments": comments,
        "publishTime": publish_time
    }
