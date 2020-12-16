from flask import Blueprint, request, jsonify
from exts import db
from .models import Club, User
from app.utils import get_club_info


club_queries = Blueprint('club_queries', __name__)

@club_queries.route('/club/query/admin', methods=['GET'])
def query_admin():
    userId = request.args.get('userId')
    user = User.query.filter_by(id=userId).first()
    if not user:
        return 'wrong userId'
    else:
        return {"clubSummary": get_club_info(user.owned_clubs) + get_club_info(user.managed_clubs)}


@club_queries.route('/club/query/followed', methods=['GET'])
def query_followed():
    userId = request.args.get('userId')
    user = User.query.filter_by(id=userId).first()
    if not user:
        return 'wrong userId'
    else:
        return {"clubSummary": get_club_info(user.followed_clubs)}
