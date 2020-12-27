from flask import Blueprint, request, jsonify
from .models import User, Club, Post
from .utils import get_club_info, get_post_info
image = Blueprint('image', __name__)

basedir = os.path.abspath(os.path.dirname(__file__))

@image.route('/image/upload', methods=['POST'])
def upload_image():
    img = request.files.get('img')
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    img_name = img.filename
    url = '/static/images/' + rand_name + img_name
    path = basedir + url
    try:
        img.save(path)
    except:
        return 'database error', 500
    pic = Picture(url=url)
    try:
        db.session.add(pic)
        db.session.commit()
    except:
        return 'database error', 500
    return 'success', 200
