import json

from flask import Blueprint, request
from flask_login import login_required, logout_user

from exts import db
from .models import Club, User
from .utils import get_club_brief_info, delete_club_posts

administrator_page = Blueprint('administrator_page', __name__)


@administrator_page.route('/systemAdmin/homepage', methods=['GET'])
@login_required
def load_systemAdmin_page():
    if False:   # illegal access
        return "illegal access", 403
    else:
        clubs = Club.query.all()
        club_list = get_club_brief_info(clubs)
        return {'clubSummary': club_list}, 200


@administrator_page.route('/systemAdmin/homepage/addClub', methods=['POST'])
@login_required
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
@login_required
def delete_club():
    club_name = (json.loads(request.get_data(as_text=True))).get('clubName')
    club = Club.query.filter_by(club_name=club_name).first()
    if not club:
        return 'invalid clubname', 403

    delete_club_posts(club)
    db.session.delete(club)
    db.session.commit()
    return 'success', 200


@administrator_page.route('/systemAdmin/homepage/changeClubPresident', methods=['POST'])
@login_required
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
@login_required
def system_admin_logout():
    logout_user()
    return 'success', 200
