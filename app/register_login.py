import smtplib
from flask import Blueprint, request, session
from flask_mail import Message
from exts import db, cache, mail
from .models import User
from decorators import login_required
import numpy as np
register_login = Blueprint('register_login', __name__, url_prefix='/user')


@register_login.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'wrong username', 300
    if user.password == password:
        if session.get('user_id'):
            return 'multiple login error'
        session['user_id'] = user.id
        return 'valid'
    else:
        return 'wrong password', 300


@register_login.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    captcha = request.form.get('captcha')
    print(cache)
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
@login_required
def logout():
    user_id = request.form.get('userId', type=int)
    if session.get('user_id') != user_id:
        return 'invalid userId'
    session.pop('userId', None)
    return 'success', 200
