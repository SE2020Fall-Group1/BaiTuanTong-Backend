import json
import pytest
from exts import db
from manage import app
from tests.utils import add_items


@pytest.fixture
def client(request):
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():  # 每个测试运行后都会执行该函数
        app.config['TESTING'] = False

    request.addfinalizer(teardown)  # 执行回收函数
    return client


def get_admin(client, club_id):
    url = '/club/admin?clubId=%d' % club_id
    return client.get(url, follow_redirects=True)


def add_admin(client, club_id, username):
    url = '/club/admin/add'
    return client.post(
        url,
        data=json.dumps(dict(clubId=club_id, username=username))
    )


def delete_admin(client, club_id, user_id):
    url = '/club/admin/delete'
    return client.post(
        url,
        data=json.dumps(dict(clubId=club_id, userId=user_id))
    )


class Test_get_admin:
    def test_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_items()

    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = get_admin(client, 1)
        print(rv.data)
        assert rv.json == {'adminSummary': [{'userId': 2, 'username': 'gf'}]}


class Test_add_admin:
    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = add_admin(client, 1, 'jhc')
        assert rv.data == b'user owned the club'

    def test2(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = add_admin(client, 2, 'jhc')
        assert rv.data == b'success'

    def test3(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = add_admin(client, 1, 'gf')
        assert rv.data == b'user managed the club'

    def test4(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = add_admin(client, 1, 'jjjjhhhhccc')
        assert rv.data == b'invalid username'

    def test5(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = add_admin(client, 4, 'gf')
        assert rv.data == b'invalid clubId'


class Test_delete_admin:
    def test1(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = delete_admin(client, 1, 1)
        assert rv.data == b'no management error'

    def test2(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = delete_admin(client, 2, 1)
        assert rv.data == b'success'

    def test4(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = delete_admin(client, 1, 4)
        assert rv.data == b'invalid userId'

    def test5(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        rv = delete_admin(client, 3, 2)
        assert rv.data == b'invalid clubId'


if __name__ == '__main__':
    pytest.main(['-s', 'test_club_admin_manage.py'])
