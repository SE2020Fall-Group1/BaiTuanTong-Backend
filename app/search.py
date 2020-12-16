from flask import Blueprint, request, jsonify
from .models import User, Club, Post
from .utils import get_club_info, get_post_info
search = Blueprint('search', __name__)


@search.route('/club/search', methods=['GET'])
def search_club():
    keyword = request.args.get('keyword')
    clubs = Club.query.filter(Club.club_name.contains(keyword)).all()
    return {"clubSummary": get_club_info(clubs)}


@search.route('/post/search', methods=['GET'])
def search_post():
    keyword = request.args.get('keyword')
    posts = Post.query.filter(Post.title.contains(keyword)).all()
    print(keyword)
    print(posts)
    return {"postSummary": get_post_info(posts, sort_key='likeCnt')}
