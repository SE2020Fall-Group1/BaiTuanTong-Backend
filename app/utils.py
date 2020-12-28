import os
import random
import string
from PIL import Image

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


def get_post_info(posts, sort_key=None, max_num=None):
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
        if max_num and max_num < len(ret_info):
            ret_info = random.sample(ret_info[:max_num * 2], max_num)
    return ret_info


def save_image(image, prefix, make_tiny=False):
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    image_name = image.filename
    url = os.path.join(prefix, rand_name + image_name)
    path = os.path.join(basedir, '..', 'static', 'images', url)
    image.save(path)
    if make_tiny:
        tiny_img = Image.open(image.stream)
        tiny_img = tiny_img.resize((100, 100))
        path = os.path.join(basedir, '..', 'static', 'images', 'tiny', url)
        tiny_img.save(path)
    return url


def delete_image(image):
    if image is not None:
        path = basedir + '/..' + image.url
        if os.path.exists(path):
            os.remove(path)
        db.session.delete(image)
