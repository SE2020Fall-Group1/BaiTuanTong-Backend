from flask import Flask

app = Flask(__name__)   # 通过装饰器设置路由方法


@app.route('/test/hello')
def hello_world():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
    # 默认debug=False, host=127.0.0.1，port=8888, 基于werkzeug实现
    # werkzeug中的run_sample(host, port, app)
