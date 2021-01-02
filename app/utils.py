import datetime
import os
import random
import string

from PIL import Image

from exts import db

basedir = os.path.abspath(os.path.dirname(__file__))


def time2str(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_user_info(users):
    ret_info = []
    for user in users:
        ret_info.append({"userId": user.id,
                         "username": user.username})
    return ret_info


def get_club_info(clubs):
    ret_info = []
    for club in clubs:
        if club.image:
            clubImageUrl = club.image.url
        else:
            clubImageUrl = None
        ret_info.append({"clubId": club.id,
                         "clubName": club.club_name,
                         "introduction": club.introduction,
                         "president": club.president.username,
                         "clubImage": clubImageUrl})
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
        if post.club.image:
            clubImageUrl = post.club.image.url
        else:
            clubImageUrl = None
        ret_info.append({"postId": post.id,
                         "title": post.title,
                         "text": post.text,
                         "clubId": post.club.id,
                         "clubName": post.club.club_name,
                         "likeCnt": len(post.likes.all()),
                         "commentCnt": len(post.comments.all()),
                         "publishTime": time2str(post.publish_time),
                         "clubImage": clubImageUrl})
    if sort_key:
        ret_info = sorted(ret_info, key=lambda x: x[sort_key], reverse=True)
        if max_num and max_num < len(ret_info):
            ret_info = random.sample(ret_info[:max_num * 2], max_num)
    return ret_info


def crop_image(img, new_w, new_h):
    w, h = img.size
    left = (w - new_w) / 2
    top = (h - new_h) / 2
    right = (w + new_w) / 2
    bottom = (h + new_h) / 2
    return img.crop((left, top, right, bottom))


def crop_and_resize(img, size):
    min_size = min(img.size)
    img = crop_image(img, min_size, min_size)
    return img.resize((size, size))


def save_image(image, prefix, max_size=None, make_tiny=False):
    rand_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    ext_name = image.filename.rsplit('.', 1)[1]
    url = os.path.join(prefix, rand_name + '_' +
                       str(datetime.datetime.now()).replace(' ', '_').replace(':', '') + '.' + ext_name)
    path = os.path.join(basedir, '..', 'static', 'images', url)
    img = Image.open(image.stream)
    if max_size:
        img = crop_and_resize(img, max_size)
    img.save(path)
    if make_tiny:
        tiny_img = crop_and_resize(img, 50)
        path = os.path.join(basedir, '..', 'static', 'images', 'tiny', url)
        tiny_img.save(path)
    return url


def delete_image(image):
    if image is not None:
        path = os.path.join(basedir, '..', 'static', 'images', image.url)
        if os.path.exists(path):
            os.remove(path)
        path = os.path.join(basedir, '..', 'static', 'images', 'tiny', image.url)
        if os.path.exists(path):
            os.remove(path)
        db.session.delete(image)
