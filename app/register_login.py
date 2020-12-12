import smtplib
from flask import Blueprint, request
from flask_mail import Message
from exts import db, cache, mail
from .models import User
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
        return 'valid'
    else:
        return 'wrong password', 300


@register_login.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    if User.query.filter_by(username=username).first():
        return 'username existed', 300
    elif User.query.filter_by(email=email).first():
        return 'email existed', 300
    else:
        user = User(username=username,
                    password=password,
                    email=email)
        db.session.add(user)
        db.session.commit()
        return 'user established'


@register_login.route('/captcha', methods=['GET'])
def email_captcha():
    email_address = request.args.get('email_address')
    if not email_address:
        return 'empty address', 400
    captcha = ''.join(map(str, np.random.randint(0, 10, 6)))
    if cache.get(email_address):
        return 'click too frequently'
    msg = Message('百团通注册验证码', recipients=[email_address], body='您的验证码是：%s' % captcha)
    try:
        mail.send(msg)
    except smtplib.SMTPException:
        return 'sending failed', 500
    cache.set(email_address, captcha)
    return 'success', 200
