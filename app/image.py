from flask import Blueprint, request
from .models import Picture, User, Club, Post
from .utils import save_image, delete_image
from exts import db
image = Blueprint('image', __name__)


@image.route('/user/image/upload', methods=['POST'])
def upload_user_image():
    userId = request.form.get('userId')
    user = User.query.filter_by(id=userId).one_or_none()
    if not user:
        return 'invalid userId', 400
    
    image = request.files.get('image')
    try:
        url = save_image(image, prefix='user', make_tiny=True)
    except Exception as e:
        print(e)
        return str(e), 500

    pic = Picture(url=url, user_id=userId)
    try:
        delete_image(user.image)
        db.session.add(pic)
        db.session.commit()
    except Exception as e:
        print(e)
        return 'database error', 500

    return 'success', 200


@image.route('/user/image/download', methods=['GET'])
def download_user_image():
    userId = request.args.get('userId')
    user = User.query.filter_by(id=userId).one_or_none()
    if not user:
        return 'invalid userId', 400
    if not user.image:
        return 'no user image', 400
    return user.image.url, 200


@image.route('/club/image/upload', methods=['POST'])
def upload_club_image():
    clubId = request.form.get('clubId')
    club = Club.query.filter_by(id=clubId).one_or_none()
    if not club:
        return 'invalid clubId', 400
    
    image = request.files.get('image')
    url = save_image(image, prefix='club', make_tiny=True)
    pic = Picture(url=url, club_id=clubId)
    try:
        delete_image(club.image)
        db.session.add(pic)
        db.session.commit()
    except Exception as e:
        print(e)
        return 'database error', 500
    
    return 'success', 200


@image.route('/club/image/download', methods=['GET'])
def download_club_image():
    clubId = request.args.get('clubId')
    club = Club.query.filter_by(id=clubId).one_or_none()
    if not club:
        return 'invalid clubId', 400
    if not club.image:
        return 'no club image', 400
    return club.image.url, 200