import os, random, string
from exts import db
basedir = os.path.abspath(os.path.dirname(__file__))

def get_user_info(users):
    ret_info = []
    for user in users:
        ret_info.append({"userId": user.id,
                         "username": user.username})
    return ret_info


def get_club_info(clubs):
    ret_info = []
    for club in clubs:
        ret_info.append({"clubId": club.id,
                         "clubName": club.club_name,
                         "introduction": club.introduction,
                         "president": club.president.username})
    return ret_info


def get_club_brief_info(clubs):
    ret_info = []
    for club in clubs:
        ret_info.append({"clubName": club.club_name,
                         "president": club.president.username})
    return ret_info


def get_post_info(posts, sort_key=None):
    ret_info = []
    for post in posts:
        ret_info.append({"postId": post.id,
                         "title": post.title,
                         "text": post.text,
                         "clubId": post.club.id,
                         "clubName": post.club.club_name,
                         "likeCnt": len(post.likes.all()),
                         "commentCnt": len(post.comments.all()),
                         "publishTime": post.publish_time})
    if sort_key:
        ret_info = sorted(ret_info, key=lambda x: x[sort_key], reverse=True)
    return ret_info


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
        if os.path.exists(path):
            os.remove(path)
        db.session.delete(image)