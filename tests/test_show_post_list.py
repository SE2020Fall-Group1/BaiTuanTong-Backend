from manage import app
from .utils import add_items
from exts import db

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


def push_homepage(client, user_id):
    url = '/post/homepage?userId=%d' % user_id
    return client.get(url, follow_redirects=True)


def push_followed(client, user_id):
    url = '/post/followed?userId=%d' % user_id
    return client.get(url, follow_redirects=True)


def push_collection(client, user_id):
    url = '/post/collection?userId=%d' % user_id
    return client.get(url, follow_redirects=True)


class Test_push_followed:
    def test_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test1(self, client):
        rv = push_followed(client, 1)
        response = rv.json
        print(rv.data)
        for post in response['postSummary']:
            post.pop('publishTime')
        assert response == {"postSummary": [
            {"postId": 1, "title": "one", "clubId": 1, "clubName": "yuanhuo", "text": "jd is too strong", "likeCnt": 1,
             "commentCnt": 1}]
        }


class Test_push_homepage:
    def test1(self, client):
        rv = push_homepage(client, 1)
        response = rv.json
        print(rv.data)
        for post in response['postSummary']:
            post.pop('publishTime')
        assert response == {"postSummary": [
            {"postId": 1, "title": "one", "clubId": 1, "clubName": "yuanhuo", "text": "jd is too strong", "likeCnt": 1,
             "commentCnt": 1},
            {'clubId': 2, 'clubName': 'feiying', 'commentCnt': 0, 'likeCnt': 0, 'postId': 2,
             'text': "let's compliment jd", 'title': 'two'},
            {'clubId': 2, 'clubName': 'feiying', 'commentCnt': 0, 'likeCnt': 0, 'postId': 3,
             'text': 'why not compliment jd', 'title': 'three'}
        ]}


class Test_push_collection:
    def test1(self, client):
        rv = push_collection(client, 2)
        response = rv.json
        print(rv.data)
        for post in response['postSummary']:
            post.pop('publishTime')
        assert response == {"postSummary": [
            {'clubId': 2, 'clubName': 'feiying', 'commentCnt': 0, 'likeCnt': 0, 'postId': 3,
             'text': "why not compliment jd", 'title': 'three'}]}
