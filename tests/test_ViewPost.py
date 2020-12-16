import json
from manage import app
from exts import db
from tests.utils import add_items
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


def viewPost(client, user_id, post_id):
    url = '/post/view?userId=%s&postId=%s' % (user_id, post_id)
    return client.get(
        url,
        follow_redirects=True
    )
    # 当请求返回后会跳转页面时，要用follow_redirects=True告诉客户端追踪重定向


# 类名必须以Test_开头，函数名必须以test_开头
# 目前的测试只是打印出了几个情况的返回值（需要-s选项）
class Test_ViewPost:
    def test_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = viewPost(client, 1, 1)
        print(rv.data)
        response = rv.json
        assert 'publishTime' in response
        response.pop('publishTime')
        assert response == {"clubName": "yuanhuo", "comments": [{"commenterUsername": "zhp", "content": "i think so."}],
                            "content": "jd is too strong", "isLiked": True, "likeCnt": 1, "postId": "1",
                            "title": "one"}

    def test2(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = viewPost(client, 2, 1)
        print(rv.data)
        response = rv.json
        assert 'publishTime' in response
        response.pop('publishTime')
        assert response == {"clubName": "yuanhuo", "comments": [{"commenterUsername": "zhp", "content": "i think so."}],
                            "content": "jd is too strong", "isLiked": False, "likeCnt": 1, "postId": "1",
                            "title": "one"}

    def test3(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = viewPost(client, 1, 3)
        print(rv.data)
        assert rv.data == b'invalid postId'


if __name__ == '__main__':
    pytest.main(['-s', 'test_ViewPost.py'])
