from .models import User

def get_user_info(users):
    ret_info = []
    for user in users:
        ret_info.append({"userId": user.id,
                         "username": user.username})
    return ret_info


def get_club_info(clubs):
    ret_info = []
    for club in clubs:
        ret_info.append({"clubId": club.id,
                         "clubName": club.club_name,
                         "introduction": club.introduction,
                         "president": club.president.username})
    return ret_info


def get_post_info(posts):
    ret_info = []
    for post in posts:
        ret_info.append({"postId": post.id,
                         "title": post.title,
                         "text": post.text,
                         "clubId": post.club.id,
                         "clubName": post.club.club_name,
                         "likeCnt": len(post.likes.all()),
                         "commentCnt": len(post.comments.all())})
    ret_info = sorted(ret_info, key=lambda x: x['likeCnt'], reverse=True)
    return ret_info
