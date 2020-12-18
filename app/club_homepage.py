import json
from flask import Blueprint, request, json
from .models import Club, User
from exts import db
from decorators import id_mapping
club_homepage = Blueprint('club_homepage', __name__)


def club_posts(posts):
    ret_info = []
    for post in posts:
        ret_info.append({'title': post.title, 'text': post.text, 'postId': post.id})
    return ret_info


@club_homepage.route('/club/homepage', methods=['GET'])
@id_mapping('clubId')
def load_homepage(club, request_form):
    introduction = club.introduction
    president = club.president
    postSummary = club_posts(club.posts)
    return {'clubName': club.club_name, 'introduction': introduction, 'president': president.username, 'postSummary': postSummary}, 200


@club_homepage.route('/club/homepage/changeIntroduction', methods=['POST'])
@id_mapping('clubId')
def change_introduction(club, request_form):
    new_introduction = request_form.get('newIntroduction')
    club.introduction = new_introduction
    db.session.commit()
    return 'success', 200

