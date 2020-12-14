import json
from exts import db
from flask import Blueprint, request, jsonify, make_response
from .models import Club, User
administrator_page = Blueprint('administrator_page', __name__)


def clubs_info(clubs):
    ret_info = []
    for club in clubs:
        president_name = User.query.filter_by(id=club.president_id).first().username
        ret_info.append({
            'clubName': club.club_name,
            'president_name': president_name
        })
    return ret_info


@administrator_page.route('/administrator/homepage', methods=['GET'])
def load_homepage():
    if False:   # illegal access
        return {'error': "illegal access"}
    else:
        clubs = Club.query.all()
        # clubs = db.session.query(Club).all()
        club_list = clubs_info(clubs)
        return {'clubSummary': club_list}
        # response.status_code = 200
