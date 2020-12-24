import json
from exts import db
from flask import Blueprint, request, jsonify, make_response, session
from .models import Club, User
from .utils import get_club_brief_info
administrator_page = Blueprint('administrator_page', __name__)


@administrator_page.route('/systemAdmin/homepage', methods=['GET'])
def load_systemAdmin_page():
    if False:   # illegal access
        return "illegal access", 403
    else:
        clubs = Club.query.all()
        # clubs = db.session.query(Club).all()
        club_list = get_club_brief_info(clubs)
        return {'clubSummary': club_list}, 200


@administrator_page.route('/systemAdmin/homepage/addClub', methods=['POST'])
def add_club():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if club:
        return 'club name used', 403

    president_name = (json.loads(request.get_data(as_text=True))).get('president')
    president = User.query.filter_by(username=president_name).first()
    if not president:
        return 'invalid username', 403

    president_id = president.id
    c1 = Club(club_name=club_name, president_id=president_id)
    db.session.add_all([c1])
    db.session.commit()
    return 'success', 200


@administrator_page.route('/systemAdmin/homepage/deleteClub', methods=['POST'])
def delete_club():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return 'invalid clubname', 403

    db.session.delete(club)
    db.session.commit()
    return 'success', 200


@administrator_page.route('/systemAdmin/homepage/changeClubPresident', methods=['POST'])
def change_club_president():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return 'invalid clubname', 403

    new_president_name = (json.loads(request.get_data(as_text=True))).get('president')
    president = User.query.filter_by(username=new_president_name).first()
    if not president:
        return 'invalid username', 403

    club.president_id = president.id
    db.session.commit()
    return 'success', 200


@administrator_page.route('/systemAdmin/logout', methods=['POST'])
def system_admin_logout():
    if not session.get('systemAdmin_login'):
        return 'invalid operation', 403
    session.pop('systemAdmin_login')
    return 'success', 200
