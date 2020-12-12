from exts import db
from app.models import User, Preference, Club, Post, Like, Comment

def add_items():
    u1 = User(username='jhc', password='hehe', email='jhc@pku.edu.cn')
    u2 = User(username='gf', password='gaga', email='gf@stu.pku.edu.cn')
    u3 = User(username='zhp', password='hail', email='zhp@pku.edu.cn')

    pr1 = Preference(preference_name='kfc')

    c1 = Club(club_name='yuanhuo', president_id=1)
    c2 = Club(club_name='feiying', president_id=2)

    po1 = Post(title='one', text='jd is too strong', club_id=1)
    po2 = Post(title='two', text="let's compliment jd", club_id=2)

    co1 = Comment(user_id=3, post_id=1, content='i think so.')

    like1 = Like(user_id=1, post_id=1)

    u1.preferences.append(pr1)
    u1.followed_clubs.append(c1)
    u2.managed_clubs.append(c1)

    po1.likes.append(like1)

    db.session.add_all([u1, u2, u3, pr1, po1, po2, co1, like1, c1, c2])
    db.session.commit()
