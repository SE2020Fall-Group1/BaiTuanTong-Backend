from flask import Blueprint, request, jsonify
from .models import Picture, User, Preference, Club, Post, Like
from exts import db
import os, sys, random, string
image = Blueprint('image', __name__)

basedir = os.path.abspath(os.path.dirname(__file__))

@image.route('/image/upload', methods=['POST'])
def upload_image():
    img = request.files.get('img')
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    img_name = img.filename
    url = '/static/images' + rand_name + img_name
    path = basedir + '/..' + url
    try:
        img.save(path)
    except:
        return 'database error', 500
    pic = Picture(url=url)
    print(pic)
    try:
        db.session.add(pic)
        db.session.commit()
    except:
        return 'database error', 500
    return 'success', 200

@image.route('/user/image/upload', methods=['POST'])
def upload_user_image():
    userId = request.form.get('userId')
    user = User.query.filter_by(id=userId).one_or_none()
    if not user:
        return 'invalid userId', 400
    
    img = request.files.get('image')
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    img_name = img.filename
    url = '/static/images/' + rand_name + img_name
    path = basedir + '/..' + url
    try:
        img.save(path)
    except:
        return 'database error', 500
    pic = Picture(url=url, user_id=userId)
    print(pic)
    try:
        db.session.add(pic)
        db.session.commit()
    except:
        return 'database error', 500
    
    return 'success', 200

@image.route('/user/image/download', methods=['GET'])
def download_user_image():
    userId = request.args.get('userId')
    user = User.query.filter_by(id=userId).one_or_none()
    if not user:
        return 'invalid userId', 400
    return user.image.url, 200