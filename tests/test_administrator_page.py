from exts import db
from app.models import User, Preference, Club, Post
from manage import app
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


def load_systemAdmin_page(client):
    url = '/systemAdmin/homepage'
    return client.get(
        url
    )


def add_club(client, clubName, president):
    url = '/systemAdmin/homepage/addClub'
    return client.post(
        url,
        data=json.dumps(dict(clubName=clubName, president=president))
    )


def delete_club(client, clubName):
    url = '/systemAdmin/homepage/deleteClub'
    return client.post(
        url,
        data=json.dumps(dict(clubName=clubName))
    )


def change_club_president(client, clubName, president):
    url = '/systemAdmin/homepage/changeClubPresident'
    return client.post(
        url,
        data=json.dumps(dict(clubName=clubName, president=president))
    )


class Test_systemAdmin_page:

    def test_systemAdmin_page(self, client, init_db):
        rv = load_systemAdmin_page(client)
        print("\n")
        print(rv.data)
        clubSummary = rv.json.get('clubSummary')
        assert clubSummary[0] == {'clubName': 'yuanhuo', 'president_name': 'tl'}
        assert clubSummary[1] == {'clubName': 'feiying', 'president_name': 'dgl'}
        # data == json.loads(rv.data)


class Test_add_club:

    def test_president_doNotExist(self, client, init_db):
        rv = add_club(client, 'go', 'lyp')
        print(rv.data)
        assert rv.data == b'invalid username'

    def test_club_exist(self, client, init_db):
        rv = add_club(client, 'yuanhuo', 'tl')
        print(rv.data)
        assert rv.data == b'club name used'

    def test_correct(self, client, init_db):
        rv = add_club(client, 'fenglei', 'tl')
        print(rv.data)
        assert rv.data == b'success'


class Test_delete_club:

    def test_club_doNotExist(self, client, init_db):
        rv = delete_club(client, 'tianmao')
        print(rv.data)
        assert rv.data == b'invalid clubname'

    def test_correct(self, client, init_db):
        rv = delete_club(client, 'fenglei')
        print(rv.data)
        assert rv.data == b'success'

    def test_club_deleted(self, client, init_db):
        rv = delete_club(client, 'fenglei')
        print(rv.data)
        assert rv.data == b'invalid clubname'


class Test_change_club_president:

    def test_club_doNotExist(self, client, init_db):
        rv = change_club_president(client, 'boxing', 'dgl')
        print(rv.data)
        assert rv.data == b'invalid clubname'

    def test_president_doNotExist(self, client, init_db):
        rv = change_club_president(client, 'yuanhuo', 'lt')
        print(rv.data)
        assert rv.data == b'invalid username'

    def test_correct(self, client, init_db):
        with app.app_context():
            club = Club.query.filter_by(club_name='yuanhuo').first()
            president = User.query.filter_by(id=club.president_id).first()
            print(president.username)
            assert president.username == 'tl'

        rv = change_club_president(client, 'yuanhuo', 'dgl')
        print(rv.data)
        assert rv.data == b'success'

        with app.app_context():
            club = Club.query.filter_by(club_name='yuanhuo').first()
            president = User.query.filter_by(id=club.president_id).first()
            print(president.username)
            assert president.username == 'dgl'


if __name__ == '__main__':
    pytest.main(['-s', 'test_administrator_page.py'])
