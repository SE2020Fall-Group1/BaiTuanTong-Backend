import json
from flask import Blueprint, request, json
from .models import Club, User
from app.utils import get_user_info
from exts import db
from decorators import id_mapping
club_admin_manage = Blueprint('club_admin_manage', __name__, url_prefix='/club/admin')


@club_admin_manage.route('/', methods=['GET'])
@id_mapping(['club'])
def get_admin(club, request_form):
    return {"adminSummary": get_user_info(club.managing_users)}, 200


@club_admin_manage.route('/add', methods=['POST'])
def add_admin():
    request_form = json.loads(request.get_data(as_text=True))
    username = request_form.get('username')
    club_id = request_form.get('clubId')
    user = User.query.filter_by(username=username).one_or_none()
    if not user:
        return 'invalid username', 400
    club = Club.query.filter_by(id=club_id).one_or_none()
    if not club:
        return 'invalid clubId', 400
    if club in user.owned_clubs:
        return 'user owned the club', 400
    if club in user.managed_clubs:
        return 'user managed the club', 400
    user.managed_clubs.append(club)
    db.session.commit()
    return 'success', 200


@club_admin_manage.route('/delete', methods=['POST'])
@id_mapping(['user', 'club'])
def delete_admin(user, club, request_form):
    if club not in user.managed_clubs:
        return 'no management error', 400
    user.managed_clubs.remove(club)
    db.session.commit()
    return 'success', 200
