from flask_script import Manager
from exts import db
from app.models import User, Preference, Club, Post
from manage import app
import requests


manager = Manager(app)


class HttpRequest(object):
    """不记录任何的请求方法"""

    @classmethod
    def request(cls, method, url, data=None, headers=None): # 这里是要传入的参数，请求方法、接口地址、传参、头文件
        method = method.upper() # 这里将传入的请求方法统一大写，然后进行判断采用什么方法
        if method == 'POST':
            return requests.post(url=url, data=data, headers=headers)
        elif method == 'GET':
            return requests.get(url=url, params=data, headers=headers)


class HttpSession(object):
    """记录Session的方法"""
    def __init__(self):
        self.session = requests.session() # 初始化一个保存session的方法

    def request(self, method, url, data=None, headers=None):
        method = method.upper()
        if method == 'POST':
            return self.session.post(url=url, data=data, headers=headers)
        elif method == 'GET':
            return self.session.get(url=url, params=data, headers=headers)

    def close(self):
        """断开session连接的方法"""
        self.session.close()


@manager.command
def test_register():
    loginURL = 'http://127.0.0.1:5000/user/login'
    registerURL = 'http://127.0.0.1:5000/user/register'
    http = HttpSession()
    http1 = http.request(method='post', url=registerURL,
                         data={'username': "jhc", 'password': 'hehe'})
    http2 = http.request(method='post', url=registerURL,
                         data={'username': "gf", 'password': "hehe"})
    http3 = http.request(method='post', url=registerURL,
                         data={'username': "jd", 'password': "hehe", 'email': "789"})
    print(http1.text)
    print(http2.text)
    print(http3.text)


@manager.command
def test_database():
    db.drop_all()
    db.create_all()
    def add_items():
        u1 = User(username='jhc', password='hehe', email='jdtql@pku.com')
        u2 = User(username='gf', password='gaga', email='tqljd@pku.com')

        p1 = Preference(preference_name='kfc')
        p2 = Preference(preference_name='cpp')
        p3 = Preference(preference_name='java')

        c1 = Club(club_name='yuanhuo', president_id=1)
        c2 = Club(club_name='feiying', president_id=2)

        po1 = Post(title='one', text='jd is too strong', club_id=1)
        po2 = Post(title='two', text="let's compliment jd", club_id=2)

        u1.preferences.append(p1)
        u1.preferences.append(p2)
        u2.preferences.append(p1)
        u2.preferences.append(p3)
        u1.followed_clubs.append(c1)
        u2.managed_clubs.append(c1)

        db.session.add_all([u1, u2, p1, p2, p3, po1, po2, c1, c2])
        db.session.commit()

    add_items()
    for name in ['jhc', 'gf']:
        print(name)
        u = User.query.filter_by(username=name).first()
        for p in u.preferences:
            print(p.preference_name, end=' ')
        print()
        print('followed club: ', end='')
        for c in u.followed_clubs:
            print(c.club_name, end=' ')
        print()
        print('managed club: ', end='')
        for c in u.managed_clubs:
            print(c.club_name, end=' ')
        print()
        print(u.owned_club.club_name if u.owned_club else None)
        print()
        print('managed club: ', end='')
        for c in u.managed_clubs:
            print(c.club_name, end=' ')
        print()

    for name in ['yuanhuo', 'feiying']:
        print(name)
        c = Club.query.filter_by(club_name=name).first()
        for p in c.posts:
            print(p.title)
            print(p.text)


if __name__ == '__main__':
    manager.run()
