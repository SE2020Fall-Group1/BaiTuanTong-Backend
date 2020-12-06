import json
from flask import Blueprint, request, jsonify, make_response
from .models import Club, User
club_homepage = Blueprint('club_homepage', __name__)


def club_posts(posts):
    ret_info = []
    for post in posts:
        ret_info.append([post.title, post.text])
    return ret_info


@club_homepage.route('/club/homepage', methods=['POST'])
def load_homepage():
    club_name = request.form.get('club_name')
    club_obj = Club.query.filter_by(club_name=club_name).first()
    if not club_obj:
        return "Club do not exist"
    else:
        introduction = club_obj.introduction
        president = User.query.filter_by(id=club_obj.president_id).first()
        club_post_list = club_posts(club_obj.posts)
        response = jsonify({'introduction': introduction, 'president': president.username, 'club_post_list': club_post_list})
        # response.status_code = 200
        return response
