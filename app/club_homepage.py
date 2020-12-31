from flask import Blueprint
from flask_login import login_required

from decorators import id_mapping
from exts import db
from .utils import get_post_info

club_homepage = Blueprint('club_homepage', __name__)


@club_homepage.route('/club/homepage', methods=['GET'])
@id_mapping(['club', 'user'])
def load_homepage(club, user, request_form):
    introduction = club.introduction
    president = club.president
    post_summary = get_post_info(club.posts)
    is_followed = user.followed_clubs.filter_by(id=club.id).with_for_update().one_or_none() is not None
    return {
               'clubName': club.club_name,
               'introduction': introduction,
               'president': president.username,
               'isFollowed': is_followed,
               'postSummary': post_summary
           }, 200


@club_homepage.route('/club/homepage/changeIntroduction', methods=['POST'])
@login_required
@id_mapping(['club'])
def change_introduction(club, request_form):
    new_introduction = request_form.get('newIntroduction')
    club.introduction = new_introduction
    db.session.commit()
    return 'success', 200


@club_homepage.route('/club/follow', methods=['POST'])
@login_required
@id_mapping(['user', 'club'])
def follow_club(user, club, request_form):
    is_followed = user.followed_clubs.filter_by(id=club.id).with_for_update().one_or_none() is not None
    if is_followed:
        user.followed_clubs.remove(club)
        db.session.commit()
        return "follow cancelled", 200
    user.followed_clubs.append(club)
    db.session.commit()
    return 'follow committed', 200
