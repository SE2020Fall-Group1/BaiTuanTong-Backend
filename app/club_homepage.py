import json
from flask import Blueprint, request, jsonify, make_response, json
from .models import Club, User
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
    club_obj = Club.query.filter_by(club_name=club_name).first()
    if not club_obj:
        return {'data': "club do not exist"}
    else:
        introduction = club_obj.introduction
        president = User.query.filter_by(id=club_obj.president_id).first()
        postSummary = club_posts(club_obj.posts)
        return {'introduction': introduction, 'president': president.username, 'postSummary': postSummary}
        # response.status_code = 200
