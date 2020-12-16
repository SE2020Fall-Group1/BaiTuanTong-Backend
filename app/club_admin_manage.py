import json
from flask import Blueprint, request, json
from decorators import login_required
from .models import Club, User
from exts import db
club_admin_manage = Blueprint('club_admin_manage', __name__, url_prefix='/club/admin')


@club_admin_manage.route('/add', methods=['POST'])
@login_required
def add_admin():
    request_form = json.loads(request.get_data(as_text=True))
    user_id = request_form.get('userId')
    club_id = request_form.get('clubId')
    user = User.query.filter_by(id=user_id).one_or_none()
    if not user:
        return 'invalid userId', 400
    club = Club.query.filter_by(id=club_id).one_or_none()
    print(club_id, user_id)
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
@login_required
def delete_admin():
    request_form = json.loads(request.get_data(as_text=True))
    user_id = request_form.get('userId')
    club_id = request_form.get('clubId')
    user = User.query.filter_by(id=user_id).one_or_none()
    if not user:
        return 'invalid userId', 400
    club = Club.query.filter_by(id=club_id).one_or_none()
    if not club:
        return 'invalid clubId', 400
    if club not in user.managed_clubs:
        return 'no management error', 400
    user.managed_clubs.remove(club)
    db.session.commit()
    return 'success', 200
