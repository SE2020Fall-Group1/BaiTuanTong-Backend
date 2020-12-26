from exts import db
from app.models import User, Club, Post
from manage import app
from flask import jsonify
import json

import pytest


@pytest.fixture
def client(request):
    # 每个测试运行前都会执行下面这部分
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():     # 每个测试运行后都会执行该函数
        app.config['TESTING'] = False

    request.addfinalizer(teardown)  # 执行回收函数

    return client


@pytest.fixture(scope="module")
def init_db():
    with app.app_context():     # 需要用这句来加载app的上下文环境
        # 测试前按以下配置重置数据库
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


def load_club_homepage(client, clubId, userId):
    # url = '/club/homepage'
    url = '/club/homepage?clubId=%d&userId=%d' % (clubId, userId)
    return client.get(
        url
    )


def change_introduction(client, clubId, newIntroduction):
    url = '/club/homepage/changeIntroduction'
    return client.post(
        url,
        data=json.dumps(dict(clubId=clubId, newIntroduction=newIntroduction))
    )


def follow_club(client, userId, clubId):
    url = '/club/follow'
    return client.post(
        url,
        data=json.dumps(dict(userId=userId, clubId=clubId))
    )


class Test_club_homepage:

    def test_club_doNotExist(self, client, init_db):
        print('\n')
        rv = load_club_homepage(client, 3, 1)
        print(rv.data)
        assert rv.data == b"invalid clubId"

    def test_correct_followed(self, client, init_db):
        rv = load_club_homepage(client, 1, 1)
        data = rv.json
        print(data)
        clubName = data.get('clubName')
        assert clubName == 'yuanhuo'
        intro = data.get('introduction')
        assert intro == 'yuanhuo introduction'
        president = data.get('president')
        assert president == "tl"
        is_followed = data.get('isFollowed')
        assert is_followed == True

        post_summary = data.get('postSummary')
        print('\n', post_summary)
        assert post_summary[0].get('text') == 'jd is too strong'
        assert post_summary[0].get('title') == 'one'
        assert post_summary[0].get('postId') == 1
        assert post_summary[0].get('clubId') == 1
        assert post_summary[0].get('clubName') == 'yuanhuo'
        assert post_summary[0].get('commentCnt') == 0
        assert post_summary[0].get('likeCnt') == 0

        assert post_summary[1].get('text') == 'let\'s compliment jd'
        assert post_summary[1].get('title') == 'two'
        assert post_summary[1].get('postId') == 2
        assert post_summary[1].get('clubId') == 1
        assert post_summary[1].get('clubName') == 'yuanhuo'
        assert post_summary[1].get('commentCnt') == 0
        assert post_summary[1].get('likeCnt') == 0

    def test_correct_not_followed(self, client, init_db):
        rv = load_club_homepage(client, 1, 2)
        data = rv.json
        print(data)
        clubName = data.get('clubName')
        assert clubName == 'yuanhuo'
        intro = data.get('introduction')
        assert intro == 'yuanhuo introduction'
        president = data.get('president')
        assert president == "tl"
        is_followed = data.get('isFollowed')
        assert is_followed == False

        post_summary = data.get('postSummary')
        print('\n', post_summary)
        assert post_summary[0].get('text') == 'jd is too strong'
        assert post_summary[0].get('title') == 'one'
        assert post_summary[0].get('postId') == 1
        assert post_summary[0].get('clubId') == 1
        assert post_summary[0].get('clubName') == 'yuanhuo'
        assert post_summary[0].get('commentCnt') == 0
        assert post_summary[0].get('likeCnt') == 0

        assert post_summary[1].get('text') == 'let\'s compliment jd'
        assert post_summary[1].get('title') == 'two'
        assert post_summary[1].get('postId') == 2
        assert post_summary[1].get('clubId') == 1
        assert post_summary[1].get('clubName') == 'yuanhuo'
        assert post_summary[1].get('commentCnt') == 0
        assert post_summary[1].get('likeCnt') == 0

class Test_change_introduction:

    def test_club_doNotExist(self, client, init_db):
        rv = change_introduction(client, 3, 'club taobao do not exist')
        print(rv.data)
        assert rv.data == b'invalid clubId'

    def test_correct(self, client, init_db):
        with app.app_context():
            club = Club.query.filter_by(club_name='yuanhuo').first()
            print(club.introduction)
            assert club.introduction == 'yuanhuo introduction'

        rv = change_introduction(client, 1, 'new yuanhuo introduction')
        print(rv.data)
        assert rv.data == b'success'

        with app.app_context():
            club = Club.query.filter_by(id=1).first()
            print(club.introduction)
            assert club.introduction == 'new yuanhuo introduction'


class Test_change_introduction:

    def test_club_doNotExist(self, client, init_db):
        rv = change_introduction(client, 3, 'club taobao do not exist')
        print(rv.data)
        assert rv.data == b'invalid clubId'

    def test_correct(self, client, init_db):
        with app.app_context():
            club = Club.query.filter_by(club_name='yuanhuo').first()
            print(club.introduction)
            assert club.introduction == 'yuanhuo introduction'

        rv = change_introduction(client, 1, 'new yuanhuo introduction')
        print(rv.data)

        with app.app_context():
            club = Club.query.filter_by(id=1).first()
            print(club.introduction)
            assert club.introduction == 'new yuanhuo introduction'


class Test_follow_club:

    def test1(self, client):
        rv = follow_club(client, 1, 2)
        assert rv.data == b'follow committed'
        with app.app_context():
            user = User.query.filter_by(id=1).one_or_none()
            assert user.followed_clubs.filter_by(id=2).one_or_none()

    def test2(self, client):
        rv = follow_club(client, 1, 2)
        assert rv.data == b'follow cancelled'
        with app.app_context():
            user = User.query.filter_by(id=1).one_or_none()
            assert user.followed_clubs.filter_by(id=2).one_or_none() is None


if __name__ == '__main__':
    pytest.main(['-s', 'test_club_homepage.py'])
