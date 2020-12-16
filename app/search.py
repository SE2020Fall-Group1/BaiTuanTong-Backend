import json
from flask import Blueprint, request, jsonify
from exts import db
from .models import User, Club, Post
from app.utils import get_club_info, get_post_info
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
    return {"postSummary": get_post_info(posts)}


@search.route('/post/homepage', methods=['GET'])
def push_post():
    posts = Post.query.all()
    return {"postSummary": get_post_info(posts)}
