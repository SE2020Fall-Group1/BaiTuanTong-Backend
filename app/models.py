from exts import db


user_preference = db.Table(
    'user_preference',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('preference_id', db.Integer, db.ForeignKey('preference.id'), primary_key=True),
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    preferences = db.relationship('Preference', secondary=user_preference, backref=db.backref('users'))

class Preference(db.Model):
    __tablename__ = 'preference'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preference_name = db.Column(db.String(20), nullable=False, unique=True)
