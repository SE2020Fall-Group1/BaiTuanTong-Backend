import json
from manage import app
from exts import db
from .utils import add_items
from app.models import Post
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


def viewPostInfo(client, user_id, post_id):
    url = '/post/view/info?userId=%s&postId=%s' % (user_id, post_id)
    return client.get(
        url,
        follow_redirects=True
    )


def alter_like(client, user_id, post_id):
    url = '/post/view/like'
    return client.post(
        url,
        data=json.dumps(dict(userId=user_id, postId=post_id)),
        follow_redirects=True
    )


def release_comment(client, user_id, post_id, comment_text):
    url = '/post/view/comment'
    return client.post(
        url,
        data=json.dumps(dict(userId=user_id, postId=post_id, commentText=comment_text)),
        follow_redirects=True
    )



class Test_ViewPost:
    def test_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test1(self, client):
        rv = viewPost(client, 1, 1)
        print(rv.data)
        response = rv.json
        assert 'publishTime' in response
        response.pop('publishTime')
        assert response == {"clubId": 1, "clubName": "yuanhuo",
                            "comments": [{"commenterUsername": "zhp", "content": "i think so."}],
                            "content": "jd is too strong", "isLiked": True, "likeCnt": 1, "postId": 1,
                            "title": "one"}

    def test2(self, client):
        rv = viewPost(client, 2, 1)
        print(rv.data)
        response = rv.json
        assert 'publishTime' in response
        response.pop('publishTime')
        assert response == {"clubId": 1, "clubName": "yuanhuo",
                            "comments": [{"commenterUsername": "zhp", "content": "i think so."}],
                            "content": "jd is too strong", "isLiked": False, "likeCnt": 1, "postId": 1,
                            "title": "one"}

    def test3(self, client):
        rv = viewPost(client, 1, 4)
        print(rv.data)
        assert rv.data == b'invalid postId'

    def test4(self, client):
        rv = viewPost(client, 5, 2)
        print(rv.data)
        assert rv.data == b'invalid userId'


class Test_viewPostInfo:
    def test_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test1(self, client):
        rv = viewPostInfo(client, 1, 1)
        print(rv.data)
        response = rv.json
        assert response == {"isLiked": True, "likeCnt": 1, "commentCnt": 1,}

    def test2(self, client):
        rv = viewPostInfo(client, 2, 1)
        print(rv.data)
        response = rv.json
        assert response == {"isLiked": False, "likeCnt": 1, "commentCnt": 1,}

    def test3(self, client):
        rv = viewPostInfo(client, 1, 4)
        print(rv.data)
        assert rv.data == b'invalid postId'

    def test4(self, client):
        rv = viewPostInfo(client, 5, 2)
        print(rv.data)
        assert rv.data == b'invalid userId'


class Test_alter_like:
    def test1(self, client):
        rv = alter_like(client, 1, 2)
        assert rv.status_code == 200
        with app.app_context():
            post = Post.query.filter_by(id=2).one_or_none()
            assert post.likes[0].user_id == 1 and post.likes[0].post_id == 2
        rv = viewPost(client, 1, 2)
        assert rv.json['isLiked']

    def test2(self, client):
        rv = alter_like(client, 1, 1)
        assert rv.status_code == 200
        with app.app_context():
            post = Post.query.filter_by(id=1).one_or_none()
            assert not post.likes.all()


class Test_release_comment:
    def test1(self, client):
        rv = release_comment(client, 1, 2, 'no one is stronger than jd')
        assert rv.status_code == 200
        with app.app_context():
            post = Post.query.filter_by(id=2).one_or_none()
            print(post.comments)
            assert post.comments.filter_by(content='no one is stronger than jd').first().user_id == 1


if __name__ == '__main__':
    pytest.main(['-s', 'test_ViewPost.py'])
