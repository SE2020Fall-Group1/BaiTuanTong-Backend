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
        c3 = Club(club_name='yuanpei', president_id=2)

        po1 = Post(title='one', text='jd is too strong', club_id=1)
        po2 = Post(title='onekfc', text='jd is too too strong', club_id=1)
        po3 = Post(title='two', text="let's compliment jd", club_id=2)

        u1.preferences.append(p1)
        u1.followed_clubs.append(c1)
        u2.managed_clubs.append(c1)

        db.session.add_all([u1, u2, p1, po1, po2, po3, c1, c2, c3])
        db.session.commit()

    add_items()


def search_club(client, keyword):
    url = '/club/search'
    return client.post(
        url,
        data=dict(keyword=keyword),
        follow_redirects=True
    )
    # 当请求返回后会跳转页面时，要用follow_redirects=True告诉客户端追踪重定向

def search_post(client, keyword):
    url = '/post/search'
    return client.post(
        url,
        data=dict(keyword=keyword),
        follow_redirects=True
    )


# 类名必须以Test_开头，函数名必须以test_开头
# 目前的测试只是打印出了几个情况的返回值（需要-s选项）
class Test_search_club:
    def test_search_club1(self, client):
        rv = search_club(client, 'yuanhuo')
        print(rv.data)
    
    def test_search_club2(self, client):
        rv = search_club(client, 'yuan')
        print(rv.data)


class Test_search_post:
    def test_search_post1(self, client):
        rv = search_post(client, 'onekfc')
        print(rv.data)
    
    def test_search_post2(self, client):
        rv = search_post(client, 'one')
        print(rv.data)


if __name__ == '__main__':
    pytest.main(['-s', 'test_search.py'])
