import json
import pytest
from manage import app
from tests.utils import add_items
from exts import db
from app.models import Post, Club


@pytest.fixture
def client(request):
    # 每个测试运行前都会执行下面这部分
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():     # 每个测试运行后都会执行该函数
        app.config['TESTING'] = False

    request.addfinalizer(teardown)  # 执行回收函数

    return client


def release_post(client, title, text, club_id):
    url = '/post/release'
    return client.post(
        url,
        data=json.dumps(dict(title=title, text=text, clubId=club_id)),
        follow_redirects=True
    )


def delete_post(client, post_id):
    url = '/post/delete'
    return client.post(
        url,
        data=json.dumps(dict(postId=post_id)),
        follow_redirects=True
    )


def edit_post(client, post_id, title, text):
    url = '/post/edit'
    return client.post(
        url,
        data=json.dumps(dict(postId=post_id, title=title, text=text)),
        follow_redirects=True
    )


class Test_release:
    def test_init(self, client):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = release_post(client, 'who is tb', 'i am tb', 1)
        assert rv.data == b'success'
        with app.app_context():
            club = Club.query.filter_by(id=1).one_or_none()
            post = Post.query.filter_by(title='who is tb').one_or_none()
            assert post
            assert post.text == 'i am tb'
            assert post in club.posts


class Test_delete:
    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        with app.app_context():
            post_id = Post.query.filter_by(title='who is tb').first().id
        rv = delete_post(client, post_id)
        assert rv.data == b'success'
        with app.app_context():
            post = Post.query.filter_by(title='who is tb').first()
            assert not post


class Test_edit:
    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        with app.app_context():
            post_id = Post.query.all()[0].id
        rv = edit_post(client, post_id, 'jd style', 'i am jd')
        assert rv.data == b'success'
        with app.app_context():
            post = Post.query.filter_by(id=post_id).first()
            assert post.title == 'jd style' and post.text == 'i am jd'


if __name__ == '__main__':
    pytest.main(['-s', 'test_manage_post.py'])
