from exts import db
from app.models import User, Preference, Club, Post
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


def load_club_homepage(client, club_name):
    url = '/club/homepage'
    return client.post(
        url,
        data=json.dumps({'club_name': club_name})
    )

class Test_club_homepage:

    def test_club_homepage_1(self, client, init_db):
        print('\n')
        rv = load_club_homepage(client, 'fenglei')
        data = (json.loads(rv.data)).get("error")
        print(rv.data)
        assert data == "club do not exist"

    def test_club_homepage_2(self, client, init_db):
        # rv = load_club_homepage(client, 'yuanhuo')
        rv = load_club_homepage(client, 'yuanhuo')
        print(rv.data)
        data = json.loads(rv.data)
        intro = data.get('introduction')
        assert intro == 'yuanhuo introduction'
        president = data.get('president')
        assert president == "tl"


if __name__ == '__main__':
    pytest.main(['-s', 'test_club_homepage.py'])
