from flask import Flask
import config
from app import register_login, view_post
from exts import db

app = Flask(__name__)  # 通过装饰器设置路由方法
app.config.from_object(config)
app.register_blueprint(register_login.register_login)
app.register_blueprint(view_post.view_post)

db.init_app(app)

@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=False)
    # 默认debug=False, host=127.0.0.1，port=8888, 基于werkzeug实现
    # werkzeug中的run_sample(host, port, app)
