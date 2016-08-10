# -*- coding: utf-8 -*-
import requests
import cookielib
import re
import time
from PIL import Image
import os
import json

class Login:
    session = requests.session()
    url = "http://www.zhihu.com/"

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    def __init__(self, username, password):
        try:
            self.session.cookies = cookielib.LWPCookieJar(filename="ZhiHu/cookies")
            self.session.cookies.load(ignore_discard=True)
        except:
            print("Cookie 未能加载")
        self.username = username
        self.password = password

        self.postdata = {
            '_xsrf': self.get_xsrf(),
            'password': password,
            'remember_me': 'true',
        }

    def get_xsrf(self):
        index_url = 'http://www.zhihu.com'
        index_page = self.session.get(index_url, headers=self.header)
        html = index_page.text
        pattern = r'name="_xsrf" value="(.*?)"'
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]

    def get_html(self):
        r = requests.get(self.url, headers=self.header)
        for k in r.headers:
            print k, r.headers[k]

    def get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self.session.get(captcha_url, headers=self.header)
        with open('ZhiHu/captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        # 用pillow 的 Image 显示验证码
        # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
        try:
            im = Image.open('ZhiHu/captcha.jpg')
            im.show()
            im.close()
        except:
            return (u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = raw_input("please input the captcha\n>")
        return captcha

    def run(self):
        if self.is_login():
            return '您已经登录'
        else:
            # 通过输入的用户名判断是否是手机号
            if re.match(r"^1\d{10}$", self.username):
                # print("手机号登录 \n")
                post_url = 'http://www.zhihu.com/login/phone_num'
                self.postdata["phone_num"] = self.username
            else:
                # print("邮箱登录 \n")
                post_url = 'http://www.zhihu.com/login/email'
                self.postdata["email"] = self.username
            try:
                # 不需要验证码直接登录成功
                login_page = self.session.post(post_url, data=self.postdata, headers=self.header)
                login_code = login_page.text
                return_data = login_page.status, login_code
            except:
                # 需要输入验证码后才能登录成功
                self.postdata["captcha"] = self.get_captcha()
                login_page = self.session.post(post_url, data=self.postdata, headers=self.header)
                login_code = json.loads(login_page.text)
                return_data = login_code['msg']
        self.session.cookies.save()
        return return_data

    def is_login(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = "https://www.zhihu.com/settings/profile"
        try:
            login_code = self.session.get(url, allow_redirects=False, headers=self.header).status_code
            if int(x=login_code) == 200:
                return True
            else:
                return False
        except:
            return False


if __name__ == u"__main__":
    print os.path.abspath("cookies")
    # Z = ZhiHu("123207246@qq.com", "yang890414")
    # Z.login()
