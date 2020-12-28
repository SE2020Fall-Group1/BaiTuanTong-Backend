from flask import Blueprint, request
from .models import Picture, User, Club, Post
from .utils import save_image, delete_image
from exts import db
image = Blueprint('image', __name__)

def reset_db():
    db.drop_all()
    db.create_all()

    def add_items():
        u1 = User(username='tl', password='hehe', email='tl@pku.edu.cn')
        u2 = User(username='dgl', password='gaga', email='dgl@stu.pku.edu.cn')

        c1 = Club(club_name='yuanhuo', introduction="yuanhuo introduction", president_id=1)
        c2 = Club(club_name='feiying', introduction="feiying introduction", president_id=2)

        po1 = Post(title='one', text='jd is too strong', club_id=1)
        po2 = Post(title='two', text="let's compliment jd", club_id=1)

        u1.followed_clubs.append(c1)
        u2.managed_clubs.append(c1)

        db.session.add_all([u1, u2, po1, po2, c1, c2])
        db.session.commit()

    add_items()


@image.route('/image/upload', methods=['POST'])
def upload_image():
    img = request.files.get('img')
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    img_name = img.filename
    url = '/static/images/' + rand_name + img_name
    path = basedir + '/..' + url
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


@image.route('/user/image/upload', methods=['POST'])
def upload_user_image():
    userId = request.form.get('userId')
    user = User.query.filter_by(id=userId).one_or_none()
    if not user:
        return 'invalid userId', 400
    
    image = request.files.get('image')
    url = save_image(image)
    pic = Picture(url=url, user_id=userId)
    try:
        delete_image(user.image)
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
    try:
        url = user.image.url
    except:
        return 'no user image', 400
    return url, 200


@image.route('/club/image/upload', methods=['POST'])
def upload_club_image():
    clubId = request.form.get('clubId')
    club = Club.query.filter_by(id=clubId).one_or_none()
    if not club:
        return 'invalid clubId', 400
    
    image = request.files.get('image')
    url = save_image(image)
    pic = Picture(url=url, club_id=clubId)
    try:
        delete_image(club.image)
        db.session.add(pic)
        db.session.commit()
    except:
        return 'database error', 500
    
    return 'success', 200


@image.route('/club/image/download', methods=['GET'])
def download_club_image():
    clubId = request.args.get('clubId')
    club = Club.query.filter_by(id=clubId).one_or_none()
    if not club:
        return 'invalid clubId', 400
    try:
        url = club.image.url
    except:
        return 'no club image', 400
    return url, 200