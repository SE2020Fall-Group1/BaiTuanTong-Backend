from flask import Blueprint, request, jsonify
from .models import User, Club, Post
from .utils import get_club_info, get_post_info
from decorators import id_mapping
show_post_list = Blueprint('show_post_list', __name__)


@show_post_list.route('/post/homepage', methods=['GET'])
def push_homepage():
    posts = Post.query.all()
    return {"postSummary": get_post_info(posts, sort_key='likeCnt')}


@show_post_list.route('/post/followed', methods=['GET'])
@id_mapping(['user'])
def push_followed(user, request_form):
    ret_info = []
    for club in user.followed_clubs:
        ret_info += get_post_info(club.posts)
    return {"postSummary": sorted(ret_info, key=lambda x: x['publishTime'], reverse=True)}, 200


@show_post_list.route('/post/collection', methods=['GET'])
@id_mapping(['user'])
def push_collection(user, request_form):
    return {"postSummary": get_post_info(user.collected_posts)}
