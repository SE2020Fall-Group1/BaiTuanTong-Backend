from exts import db
from app.models import User, Preference, Club, Post
from manage import app

import pytest


@pytest.fixture
def client(request):
    # 每个测试运行前都会执行下面这部分
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():  # 每个测试运行后都会执行该函数
        app.config['TESTING'] = False

    request.addfinalizer(teardown)  # 执行回收函数

    return client


def add_items():
    u1 = User(username='jhc', password='hehe', email='jhc@pku.edu.cn')
    u2 = User(username='gf', password='gaga', email='gf@stu.pku.edu.cn')

    p1 = Preference(preference_name='kfc')

    c1 = Club(club_name='yuanhuo', president_id=1)
    c2 = Club(club_name='feiying', president_id=2)
    c3 = Club(club_name='yuanpei', president_id=2)

    po1 = Post(title='one', text='jd is too strong', club_id=1)
    po2 = Post(title='onekfc', text='jd is too too strong', club_id=1)
    po3 = Post(title='two', text="let's compliment jd", club_id=2)

    u1.preferences.append(p1)
    u1.followed_clubs.append(c2)
    u2.managed_clubs.append(c1)

    db.session.add_all([u1, u2, p1, po1, po2, po3, c1, c2, c3])
    db.session.commit()


def query_admin(client, userId):
    url = '/club/query/admin?userId=%d' % userId
    return client.get(
        url,
        follow_redirects=True
    )
    # 当请求返回后会跳转页面时，要用follow_redirects=True告诉客户端追踪重定向


def query_followed(client, userId):
    url = '/club/query/followed?userId=%d' % userId
    return client.get(
        url,
        follow_redirects=True
    )


# 类名必须以Test_开头，函数名必须以test_开头
# 目前的测试只是打印出了几个情况的返回值（需要-s选项）
class Test_query_admin:
    def test_init(self):
        with app.app_context():  # 需要用这句来加载app的上下文环境
            # 按以下配置重置数据库
            db.drop_all()
            db.create_all()
            add_items()

    def test_query_admin1(self, client):
        rv = query_admin(client, 1)
        print(rv.data)
        assert rv.json == [{"clubId": 2, "clubName": "yuanhuo", "introduction": None, "president": "jhc"}]

    def test_query_admin2(self, client):
        rv = query_admin(client, 2)
        print(rv.data)
        assert rv.json == [{"clubId": 1, "clubName": "feiying", "introduction": None, "president": "gf"},
                           {"clubId": 3, "clubName": "yuanpei", "introduction": None, "president": "gf"},
                           {"clubId": 2, "clubName": "yuanhuo", "introduction": None, "president": "jhc"}]


class Test_query_followed:
    def test_query_followed1(self, client):
        rv = query_followed(client, 1)
        print(rv.data)

    def test_query_followed2(self, client):
        rv = query_followed(client, 2)
        print(rv.data)


if __name__ == '__main__':
    pytest.main(['-s', 'test_club_queries.py'])
