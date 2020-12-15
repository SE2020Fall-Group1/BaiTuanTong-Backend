import json
from flask import Blueprint, request, jsonify, make_response, json
from .models import Club, User
from exts import db
club_homepage = Blueprint('club_homepage', __name__)


def club_posts(posts):
    ret_info = []
    for post in posts:
        ret_info.append({'title': post.title, 'text': post.text})
    return ret_info


@club_homepage.route('/club/homepage', methods=['GET'])
def load_homepage():
    club_name = request.args.get('clubName')
    # club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return {'data': "club do not exist"}, 403

    introduction = club.introduction
    president = User.query.filter_by(id=club.president_id).first()
    postSummary = club_posts(club.posts)
    return {'introduction': introduction, 'president': president.username, 'postSummary': postSummary}, 200


@club_homepage.route('/club/homepage/changeIntroduction', methods=['POST'])
def change_introduction():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return {'data': 'club do not exist'}, 403

    new_introduction = (json.loads(request.get_data(as_text=True))).get('newIntroduction')
    club.introduction = new_introduction
    db.session.commit()
    return {'data': 'success'}, 200
