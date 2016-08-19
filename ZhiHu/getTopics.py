#  -*- coding: utf-8 -*-
import requests
import cookielib
from bs4 import BeautifulSoup
import re
import json


class Topics:
    session = requests.session()
    url = "https://www.zhihu.com/people/sizhuren/topics"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "X-Xsrftoken": "3ba01461fb3f7aa3e3f422fb52f073c6"
    }

    def __init__(self, url):
        try:
            self.session.cookies = cookielib.LWPCookieJar(filename="cookies")
            self.session.cookies.load(ignore_discard=True)
        except Exception, e:
            print Exception, e
        self.url = url and url or self.url

    def run(self):
        r = self.session.get(self.url,  headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        htmlList = soup.find_all('div', class_='zm-profile-section-head')
        pattern = re.compile(r'关注的话题（(.*?)）', re.S)
        match = re.findall(pattern, str(htmlList))

        pattern2 = r'name="_xsrf" value="(.*?)"'
        _xsrf = re.findall(pattern2, r.text)
        datas = {
            "start": 0,
            "offset": 0
        }

        heads = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "www.zhihu.com",
                "Origin": "https://www.zhihu.com",
                "Referer": "https://www.zhihu.com/people/sizhuren/topics",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "X-Xsrftoken": _xsrf[0]
        }
        r2 = self.session.post("https://www.zhihu.com/people/sizhuren/topics", data=datas, headers=heads)

        jsonObj = json.loads(r2.text)
        pattern3 = re.compile('strong>(.*?)</strong', re.S)
        for i in re.findall(pattern3, jsonObj['msg'][1]):
            print i
        # htmlList = soup.find_all('div', class_='zm-profile-section-main')
        # pattern = re.compile('strong>(.*?)</strong', re.S)
        # resList = []
        # for i in htmlList:
        #     match = re.findall(pattern, str(i))
        #     print match[0]
        #     resList.append(match[0])

if __name__ == u"__main__":
    t = Topics("")
    t.run()
