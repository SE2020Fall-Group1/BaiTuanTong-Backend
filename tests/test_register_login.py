from exts import db
from app.models import User, Preference, Club, Post
from manage import app

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
    print("数据库初始化")
    with app.app_context():     # 需要用这句来加载app的上下文环境
        # 按以下配置重置数据库
        db.drop_all()
        db.create_all()

        def add_items():
            u1 = User(username='jhc', password='hehe', email='jhc@pku.edu.cn')
            u2 = User(username='gf', password='gaga', email='gf@stu.pku.edu.cn')

            p1 = Preference(preference_name='kfc')

            c1 = Club(club_name='yuanhuo', president_id=1)
            c2 = Club(club_name='feiying', president_id=2)

            po1 = Post(title='one', text='jd is too strong', club_id=1)
            po2 = Post(title='two', text="let's compliment jd", club_id=2)

            u1.preferences.append(p1)
            u1.followed_clubs.append(c1)
            u2.managed_clubs.append(c1)

            db.session.add_all([u1, u2, p1, po1, po2, c1, c2])
            db.session.commit()

        add_items()


def login(client, username, password):
    url = '/user/login'
    return client.post(
        url,
        data=dict(username=username, password=password),
        follow_redirects=True
    )
    # 当请求返回后会跳转页面时，要用follow_redirects=True告诉客户端追踪重定向


def register(client, username, password, email):
    url = '/user/register'
    return client.post(
        url,
        data=dict(username=username, password=password, email=email),
        follow_redirects=True
    )


# 类名必须以Test_开头，函数名必须以test_开头
# 目前的测试只是打印出了几个情况的返回值（需要-s选项）
class Test_register:
    def test_register1(self, client, init_db):
        # init_db()
        rv = register(client, 'lzh', r'heihei', r'lzh@pku.edu.cn')
        print(rv.data)
        assert b'user established' == rv.data

    def test_register2(self, client, init_db):
        rv = register(client, 'tbw', r'jojo', r'lzh@pku.edu.cn')
        print(rv.data)
        assert b'email existed' == rv.data

    def test_register3(self, client, init_db):
        rv = register(client, 'lzh', r'jojo', r'lzh2@pku.edu.cn')
        print(rv.data)
        assert b'username existed' == rv.data

    def test_register4(self, client, init_db):
        rv = register(client, 'lzh', r'heihei', r'lzh@pku.edu.cn')
        print(rv.data)
        assert b'username existed' == rv.data

    def test_register5(self, client, init_db):
        rv = register(client, 'tbw', r'jojo', r'tbw@pku.edu.cn')
        print(rv.data)
        assert b'user established' == rv.data


class Test_login:
    def test_login1(self, client, init_db):
        rv = login(client, 'lp', 'hahaha')
        print(rv.data)
        assert b'wrong username' == rv.data

    def test_login2(self, client, init_db):
        rv = login(client, 'lzh', 'heihei')
        print(rv.data)
        assert b'valid' == rv.data

    def test_login3(self, client, init_db):
        rv = login(client, 'lzh', 'gaga')
        print(rv.data)
        assert b'wrong password' == rv.data


if __name__ == '__main__':
    pytest.main(['-s', "test_register_login.py"])
