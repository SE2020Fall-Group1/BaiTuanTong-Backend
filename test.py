import requests


class HttpRequest(object):
    """不记录任何的请求方法"""

    @classmethod
    def request(cls, method, url, data=None, headers=None): # 这里是要传入的参数，请求方法、接口地址、传参、头文件
        method = method.upper() # 这里将传入的请求方法统一大写，然后进行判断采用什么方法
        if method == 'POST':
            return requests.post(url=url, data=data, headers=headers)
        elif method == 'GET':
            return requests.get(url=url, params=data, headers=headers)


class HttpSession(object):
    """记录Session的方法"""
    def __init__(self):
        self.session = requests.session() # 初始化一个保存session的方法

    def request(self, method, url, data=None, headers=None):
        method = method.upper()
        if method == 'POST':
            return self.session.post(url=url, data=data, headers=headers)
        elif method == 'GET':
            return self.session.get(url=url, params=data, headers=headers)

    def close(self):
        """断开session连接的方法"""
        self.session.close()


if __name__ == '__main__':
    loginURL = 'http://127.0.0.1:5000/user/login'
    registerURL = 'http://127.0.0.1:5000/user/register'
    http = HttpSession()
    http1 = http.request(method='post', url=registerURL,
                            data={'username': "jhc", 'password': 'hehe'})
    http2 = http.request(method='post', url=registerURL,
                            data={'username': "gf", 'password': "hehe"})
    http3 = http.request(method='post', url=registerURL,
                            data={'username': "jd", 'password': "hehe", 'email': "789"})
    print(http1.text)
    print(http2.text)
    print(http3.text)
