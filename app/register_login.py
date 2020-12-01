import json
from flask import Blueprint, request
from exts import db
from .models import User
register_login = Blueprint('register_login', __name__)


@register_login.route('/user/login', methods=['POST'])
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


@register_login.route('/user/register', methods=['POST'])
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
