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


def load_administrator_page(client):
    url = '/administrator/homepage'
    return client.post(
        url
    )

class Test_club_homepage:

    def test_administrator_page(self, client, init_db):
        rv = load_administrator_page(client)
        print("\n")
        print(rv.data)
        club_list = json.loads(rv.data).get('club_list')
        assert club_list[0] == ['yuanhuo', 'tl']
        assert club_list[1] == ['feiying', 'dgl']
        # data == json.loads(rv.data)


if __name__ == '__main__':
    pytest.main(['-s', 'test_administrator_page.py'])
