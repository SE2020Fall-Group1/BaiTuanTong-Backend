import json
from flask import Blueprint, request, json
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
    club_id = request.args.get('clubId')
    # club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(id=club_id).first()
    if not club:
        return "club do not exist"

    introduction = club.introduction
    president = club.president
    postSummary = club_posts(club.posts)
    return {'introduction': introduction, 'president': president.username, 'postSummary': postSummary}
    # response.status_code = 200


@club_homepage.route('/club/homepage/changeIntroduction', methods=['POST'])
def change_introduction():
    club_id = (json.loads(request.get_data(as_text=True))).get('clubId')
    club = Club.query.filter_by(id=club_id).first()
    if not club:
        return 'club do not exist'

    new_introduction = (json.loads(request.get_data(as_text=True))).get('newIntroduction')
    club.introduction = new_introduction
    db.session.commit()
    return 'success'
