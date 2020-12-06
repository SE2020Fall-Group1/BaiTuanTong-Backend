import json
from flask import Blueprint, request
from exts import db
from .models import User, Club, Post
search = Blueprint('search', __name__)


def extract_club_info(clubs):
    ret_info = []
    for club in clubs:
        ret_info.append([club.id,
                         club.club_name,
                         club.introduction,
                         User.query.filter_by(id=club.president_id).first().username])
    return ret_info


@search.route('/club/search', methods=['POST'])
def search_club():
    keyword = request.form.get('keyword')
    clubs = Club.query.filter(Club.club_name.contains(keyword)).all()
    print(extract_club_info(clubs))
    return json.dumps(extract_club_info(clubs))


@search.route('/post/search', methods=['POST'])
def search_post():
    keyword = request.form.get('keyword')
    posts = Post.query.filter(keyword in Post.title).all()
    return json.dumps(posts)


@search.route('/post/push', methods=['POST'])
def push_post():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    posts = []
    for keyword in user.preferences:
        posts.extend(Post.query.filter(keyword in Post.title).all())
    return json.dumps(posts)