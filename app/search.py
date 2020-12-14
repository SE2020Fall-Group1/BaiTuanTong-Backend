import json
from flask import Blueprint, request, jsonify
from exts import db
from .models import User, Club, Post
search = Blueprint('search', __name__)


def extract_club_info(clubs):
    ret_info = []
    for club in clubs:
        ret_info.append({"clubId": club.id,
                         "clubName": club.club_name,
                         "introduction": club.introduction,
                         "president": club.president.username})
    return ret_info


def extract_post_info(posts):
    ret_info = []
    for post in posts:
        ret_info.append({"postId": post.id,
                         "title": post.title,
                         "text": post.text,
                         "clubName": post.club.club_name,
                         "likeCnt": len(post.likes)})
    return sorted(ret_info, key=lambda x: x['likeCnt'], reverse=True)


@search.route('/club/search', methods=['GET'])
def search_club():
    keyword = request.args.get('keyword')
    clubs = Club.query.filter(Club.club_name.contains(keyword)).all()
    return jsonify(extract_club_info(clubs))


@search.route('/post/search', methods=['GET'])
def search_post():
    keyword = request.args.get('keyword')
    posts = Post.query.filter(Post.title.contains(keyword)).all()
    return jsonify(extract_post_info(posts))


@search.route('/post/push', methods=['GET'])
def push_post():
    posts = Post.query.all()
    return jsonify(extract_post_info(posts))
