import json
from exts import db
from flask import Blueprint, request, jsonify, make_response
from .models import Club, User
administrator_page = Blueprint('administrator_page', __name__)


def clubs_info(clubs):
    ret_info = []
    for club in clubs:
        president_name = User.query.filter_by(id=club.president_id).first().username
        ret_info.append([club.club_name, president_name])
    return ret_info


@administrator_page.route('/administrator/homepage', methods=['POST'])
def load_homepage():
    # club_name = request.form.get('club_name')
    # club_obj = Club.query.filter_by(club_name=club_name).first()
    # if not club_obj:
    #     return jsonify({'error': "club do not exist"})
    if False:
        return jsonify("illegal access")
    else:
        # clubs = session.query(Club).all()
        # clubs = Club.query.filter_by(Club.id > 0).all()
        clubs = db.session.query(Club).all()
        club_list = clubs_info(clubs);
        response = jsonify({'club_list': club_list})
        # response.status_code = 200
        return response
