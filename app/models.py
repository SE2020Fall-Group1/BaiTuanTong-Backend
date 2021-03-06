# -*- coding: utf-8 -*-
import datetime
from exts import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


user_preference = db.Table(
    'user_preference',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('preference_id', db.Integer, db.ForeignKey('preference.id'), primary_key=True),
)

user_following_club = db.Table(
    'user_following_club',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True),
)

user_managing_club = db.Table(
    'user_managing_club',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True),
)

user_collecting_post = db.Table(
    'user_collecting_post',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, index=True, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    image = db.relationship('Picture', backref=db.backref('user'), uselist=False)
    preferences = db.relationship('Preference', secondary=user_preference, backref=db.backref('users'))
    followed_clubs = db.relationship('Club', secondary=user_following_club,
                                     backref=db.backref('following_users'), lazy='dynamic')
    managed_clubs = db.relationship('Club', secondary=user_managing_club, backref=db.backref('managing_users'))
    # managed clubs excludes owned_clubs
    owned_clubs = db.relationship('Club', backref=db.backref('president'))
    collected_posts = db.relationship('Post', secondary=user_collecting_post,
                                      backref=db.backref('collecting_users'), lazy='dynamic')
    comments = db.relationship('Comment', backref=db.backref('commenter'), lazy='dynamic')


class Preference(db.Model):
    __tablename__ = 'preference'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preference_name = db.Column(db.String(20), nullable=False, unique=True)


class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(50), nullable=False, unique=True)
    introduction = db.Column(db.Text, default='社团还没有简介哦~')
    image = db.relationship('Picture', backref=db.backref('club'), uselist=False)
    president_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('Post', backref=db.backref('club'))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    title = db.Column(db.Text, nullable=False)  # length <= 100
    text = db.Column(db.Text)  # length <= 5000
    pictures = db.relationship('Picture', backref=db.backref('post'), lazy='dynamic')
    likes = db.relationship('Like', backref=db.backref('post'), lazy='dynamic')
    comments = db.relationship('Comment', backref=db.backref('post'), lazy='dynamic')
    publish_time = db.Column(db.DateTime, default=datetime.datetime.now)


class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text)  # length <= 1000
    publish_time = db.Column(db.DateTime, default=datetime.datetime.now)
