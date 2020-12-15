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


@administrator_page.route('/systemAdmin/homepage', methods=['GET'])
def load_homepage():
    if False:   # illegal access
        return {'data': "illegal access"}
    else:
        clubs = Club.query.all()
        # clubs = db.session.query(Club).all()
        club_list = clubs_info(clubs)
        return {'clubSummary': club_list}
        # response.status_code = 200


@administrator_page.route('/systemAdmin/homepage/addClub', methods=['POST'])
def add_club():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if club:
        return {'data': 'club name exist'}

    president_name = (json.loads(request.get_data(as_text=True))).get('president')
    president = User.query.filter_by(username=president_name).first()
    if not president:
        return {'data': 'president do not exist'}

    president_id = president.id
    c1 = Club(club_name=club_name, president_id=president_id)
    db.session.add_all([c1])
    db.session.commit()
    return {'data': 'success'}


@administrator_page.route('/systemAdmin/homepage/deleteClub', methods=['POST'])
def delete_club():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return {'data': 'club do not exist'}

    db.session.delete(club)
    db.session.commit()
    return {'data': 'success'}


@administrator_page.route('/systemAdmin/homepage/changeClubPresident', methods=['POST'])
def change_club_president():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return {'data': 'club do not exist'}

    new_president_name = (json.loads(request.get_data(as_text=True))).get('president')
    president = User.query.filter_by(username=new_president_name).first()
    if not president:
        return {'data': 'new president do not exist'}

    club.president_id = president.id
    return {'data': 'success'}
