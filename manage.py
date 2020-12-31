from flask import Flask
import config
from app import register_login, view_post, search, club_queries, manage_post, club_admin_manage, club_homepage, \
    administrator_page, show_post_list, image
from exts import db, cache, mail, login_manager

app = Flask(__name__)  # 通过装饰器设置路由方法
app.config.from_object(config)
app.register_blueprint(register_login.register_login)
app.register_blueprint(search.search)
app.register_blueprint(club_queries.club_queries)
app.register_blueprint(view_post.view_post)
app.register_blueprint(club_homepage.club_homepage)
app.register_blueprint(administrator_page.administrator_page)
app.register_blueprint(manage_post.manage_post)
app.register_blueprint(club_admin_manage.club_admin_manage)
app.register_blueprint(show_post_list.show_post_list)
app.register_blueprint(image.image)

db.init_app(app)
cache.init_app(app)
mail.init_app(app)
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    # 默认debug=False, host=127.0.0.1，port=8888, 基于werkzeug实现
    # werkzeug中的run_sample(host, port, app)
