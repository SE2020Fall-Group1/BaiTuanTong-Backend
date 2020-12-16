from exts import db
from app.models import User, Preference, Club, Post, Like, Comment


def add_items():
    u1 = User(id=1, username='jhc', password='hehehe', email='jhc@pku.edu.cn')
    u2 = User(id=2, username='gf', password='gagaga', email='gf@stu.pku.edu.cn')
    u3 = User(id=3, username='zhp', password='hailjd', email='zhp@pku.edu.cn')

    pr1 = Preference(preference_name='kfc')

    c1 = Club(id=1, club_name='yuanhuo', president_id=1)
    c2 = Club(id=2, club_name='feiying', president_id=2)

    po1 = Post(id=1, title='one', text='jd is too strong', club_id=1)
    po2 = Post(id=2, title='two', text="let's compliment jd", club_id=2)
    po3 = Post(id=3, title='three', text="why not compliment jd", club_id=2)

    co1 = Comment(user_id=3, post_id=1, content='i think so.')

    like1 = Like(user_id=1, post_id=1)

    u1.preferences.append(pr1)
    u1.followed_clubs.append(c1)
    u2.managed_clubs.append(c1)
    u2.collected_posts.append(po3)

    db.session.add_all([u1, u2, u3, pr1, po1, po2, po3, co1, like1, c1, c2])
    db.session.commit()
