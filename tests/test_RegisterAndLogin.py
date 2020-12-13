import pytest
from exts import db, cache
from manage import app
from tests.utils import add_items


@pytest.fixture
def client(request):
    # 每个测试运行前都会执行下面这部分
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():     # 每个测试运行后都会执行该函数
        app.config['TESTING'] = False

    request.addfinalizer(teardown)  # 执行回收函数

    return client


def login(client, username, password):
    url = '/user/login'
    return client.post(
        url,
        data=dict(username=username, password=password),
        follow_redirects=True
    )
    # 当请求返回后会跳转页面时，要用follow_redirects=True告诉客户端追踪重定向


def register(client, username, password, email, captcha):
    url = '/user/register'
    return client.post(
        url,
        data=dict(username=username, password=password, email=email, captcha=captcha),
        follow_redirects=True
    )


def send_captcha(client, email):
    url = '/user/captcha?email=%s' % email
    return client.get(
        url,
        follow_redirects=True
    )


# 类名必须以Test_开头，函数名必须以test_开头
# 目前的测试只是打印出了几个情况的返回值（需要-s选项）
class Test_register:
    def test_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test_register1(self, client):
        rv = register(client, 'lzh', r'heihei', r'lzh@pku.edu.cn', '123')
        assert rv.data == b'invalid captcha'

    def test_register2(self, client):
        cache.set('lzh@pku.edu.cn', '123')
        print(cache.get('lzh@pku.edu.cn'))
        rv = register(client, 'lzh', r'heihei', r'lzh@pku.edu.cn', '123')
        assert rv.data == b'user established'

    def test_register3(self, client):
        rv = register(client, 'tbw', r'jojo', r'lzh@pku.edu.cn', '123')
        assert rv.data == b'email existed'

    def test_register4(self, client):
        rv = register(client, 'lzh', r'jojo', r'lzh2@pku.edu.cn', '123')
        assert rv.data == b'username existed'

    def test_register5(self, client):
        rv = register(client, 'lzh', r'heihei', r'lzh@pku.edu.cn', '123')
        assert rv.data == b'username existed'

    def test_register6(self, client):
        cache.set('tbw@pku.edu.cn', '123')
        rv = register(client, 'tbw', r'jojo', r'tbw@pku.edu.cn', '123')
        assert rv.data == b'user established'


class Test_login:
    def test_login1(self, client):
        rv = login(client, 'lp', 'hahaha')
        print(rv.data)
        assert rv.data == b'wrong username'

    def test_login2(self, client):
        rv = login(client, 'lzh', 'heihei')
        print(rv.data)
        assert rv.data == b'valid'

    def test_login3(self, client):
        rv = login(client, 'lzh', 'gaga')
        print(rv.data)
        assert rv.data == b'wrong password'


class Test_captcha:
    def test1(self, client):
        rv = send_captcha(client, '1652961256@qq.com')
        print(rv)
        assert rv.data == b'success'

    def test2(self, client):
        rv = send_captcha(client, '1652961256@qq.com')
        print(rv)
        assert rv.data == b'request too frequently'


if __name__ == '__main__':
    pytest.main(['-s'])
