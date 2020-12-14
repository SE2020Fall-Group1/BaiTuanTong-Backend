import json
from flask import Blueprint, request
from exts import db
from .models import Club, User
club_queries = Blueprint('club_queries', __name__)

def get_club_info(club_list):
    ret = []
    for club in club_list:
        ret.append([club.id,
                    club.club_name,
                    club.introduction,
                    User.query.filter_by(id=club.president_id).first().username])
    return ret

@club_queries.route('/club/query/admin', methods = ['POST'])
def query_admin():
    userId = request.form.get('userId')
    user = User.query.filter_by(id=userId).first()
    if not user:
        return 'wrong userId'
    else:
        return json.dumps(get_club_info(user.managed_clubs))

@club_queries.route('/club/query/followed', methods = ['POST'])
def query_followed():
    userId = request.form.get('userId')
    user = User.query.filter_by(id=userId).first()
    if not user:
        return 'wrong userId'
    else:
        return json.dumps(get_club_info(user.followed_clubs))
