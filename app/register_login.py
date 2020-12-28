import json
import smtplib
from flask import Blueprint, request, session
from flask_mail import Message
from exts import db, cache, mail
from .models import User
import numpy as np
register_login = Blueprint('register_login', __name__, url_prefix='/user')


@register_login.route('/login', methods=['POST'])
def login():
    request_form = json.loads(request.get_data(as_text=True))
    username = request_form.get('username')
    password = request_form.get('password')

    if username == 'amdno' and password == 'it0803':   # 之后需要在服务器数据库User表中添加该特殊账户
        session['systemAdmin_login'] = True
        return 'system administrator login', 200

    user = User.query.filter_by(username=username).first()
    if not user:
        return 'wrong username', 300
    if user.password == password:
        if session.get('user_id'):
            return 'multiple login error'
        session['user_id'] = user.id
        return {'userId': user.id}, 200
    else:
        return 'wrong password', 300


@register_login.route('/register', methods=['POST'])
def register():
    request_form = json.loads(request.get_data(as_text=True))
    username = request_form.get('username')
    password = request_form.get('password')
    email = request_form.get('email')
    captcha = request_form.get('captcha')
    if User.query.filter_by(username=username).first():
        return 'username existed', 300
    elif User.query.filter_by(email=email).first():
        return 'email existed', 300
    elif captcha != cache.get(email):
        return 'invalid captcha'
    else:
        user = User(username=username,
                    password=password,
                    email=email)
        db.session.add(user)
        db.session.commit()
        return 'user established'


@register_login.route('/captcha', methods=['GET'])
def email_captcha():
    email = request.args.get('email')
    if not email:
        return 'empty address', 400
    captcha = ''.join(map(str, np.random.randint(0, 10, 6)))
    if cache.get(email):
        return 'request too frequently'
    msg = Message('百团通注册验证码', recipients=[email], body='您的验证码是：%s' % captcha)
    try:
        mail.send(msg)
    except smtplib.SMTPException:
        return 'sending failed', 500
    cache.set(email, captcha)
    return 'success', 200


@register_login.route('/logout', methods=['POST'])
def logout():
    request_form = json.loads(request.get_data(as_text=True))
    user_id = request_form.get('userId')
    if session.get('user_id') != user_id:
        return 'invalid userId'
    session.pop('userId', None)
    return 'success', 200


@register_login.route('/password', methods=['POST'])
def change_password():
    request_form = json.loads(request.get_data(as_text=True))
    userId = request_form.get('userId')
    password = request_form.get('password')
    new_password = request_form.get('new_password')
    user = User.query.filter_by(id=userId).first()
    if not user:
        return 'invalid userId', 300
    if user.password == password:
        user.password = new_password
        db.session.commit()
        return 'success', 200
    else:
        return 'wrong password', 300