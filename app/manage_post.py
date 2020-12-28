from flask import Blueprint, request
from .models import Post, Club, Picture
from exts import db
from decorators import id_mapping
import os, random, string
manage_post = Blueprint('manage_post', __name__, url_prefix='/post')
basedir = os.path.abspath(os.path.dirname(__file__))


def save_image(image):
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    image_name = image.filename
    url = '/static/images/' + rand_name + image_name
    path = basedir + '/..' + url
    image.save(path)
    return url


def delete_image(image):
    if image is not None:
        path = basedir + '/..' + image.url
        print(path)
        os.remove(path)
        db.session.delete(image)


@manage_post.route('/release', methods=['POST'])
def release_post():
    clubId = request.form.get('clubId')
    club = Club.query.filter_by(id=clubId).one_or_none()
    if not club:
        return 'invalid clubId', 400
    
    title = request.form.get('title')
    text = request.form.get('text')
    post = Post(title=title, text=text, club_id=club.id)
    try:
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    
    images = request.files.getlist('image')
    for image in images:
        url = save_image(image)
        pic = Picture(url=url, post_id=post.id)
        try:
            db.session.add(pic)
            db.session.commit()
        except:
            return 'database error', 500
    
    return 'success', 200


@manage_post.route('/delete', methods=['POST'])
@id_mapping(['post'])
def delete_post(post, request_form):
    try:
        for image in post.pictures:
            delete_image(image)
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200


@manage_post.route('/edit', methods=['POST'])
@id_mapping(['post'])
def edit_post(post, request_form):
    title = request_form.get('title')
    text = request_form.get('text')
    try:
        post.title = title
        post.text = text
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return 'success', 200

