'''
用于处理微博登录问题

version 1: log in with POST
version 2: log in with cookie
version 3: log in with proxies
'''

import requests
import rsa
import time
import re
import random
import urllib3
import base64
from urllib.parse import quote
from binascii import b2a_hex
urllib3.disable_warnings()  # 取消警告


def get_timestamp():
    return int(time.time()*1000)  # 获取13位时间戳


class LogIn():
    def __init__(self):
        self.username = 'raymondsun97@yahoo.com'
        self.password = '68458173'
        self.session = requests.session()  # 登录用session
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.session.verify = False  # 取消证书验证

    def post(self):
        # 预登录，获取一些必须的参数
        self.su = base64.b64encode(
            self.username.encode())  # 阅读js得知用户名进行base64转码
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_={}'.format(
            quote(self.su), get_timestamp())  # 注意su要进行quote转码
        response = self.session.get(url).content.decode()
        self.nonce = re.findall(r'"nonce":"(.*?)"', response)[0]
        self.pubkey = re.findall(r'"pubkey":"(.*?)"', response)[0]
        self.rsakv = re.findall(r'"rsakv":"(.*?)"', response)[0]
        self.servertime = re.findall(r'"servertime":(.*?),', response)[0]

        # 用rsa对明文密码进行加密，加密规则通过阅读js代码得知
        publickey = rsa.PublicKey(int(self.pubkey, 16), int('10001', 16))
        message = str(self.servertime) + '\t' + \
            str(self.nonce) + '\n' + str(self.password)
        self.sp = rsa.encrypt(message.encode(), publickey)

        # log in
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
            'vsnf': '1',
            'su': self.su,
            'service': 'miniblog',
            'servertime': str(int(self.servertime)+random.randint(1, 20)),
            'nonce': self.nonce,
            'pwencode': 'rsa2',
            'rsakv': self.rsakv,
            'sp': b2a_hex(self.sp),
            'sr': '1536 * 864',
            'encoding': 'UTF - 8',
            'prelt': '35',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }
        response = self.session.post(
            url, data=data, allow_redirects=False).text  # 提交账号密码等参数
        # 微博在提交数据后会跳转，此处获取跳转的url
        redirect_url = re.findall(r'location.replace\("(.*?)"\);', response)[0]
        result = self.session.get(
            redirect_url, allow_redirects=False).text  # 请求跳转页面
        ticket, ssosavestate = re.findall(
            r'ticket=(.*?)&ssosavestate=(.*?)"', result)[0]  # 获取ticket和ssosavestate参数
        uid_url = 'https://passport.weibo.com/wbsso/login?ticket={}&ssosavestate={}&callback=sinaSSOController.doCrossDomainCallBack&scriptId=ssoscript0&client=ssologin.js(v1.4.19)&_={}'.format(
            ticket, ssosavestate, get_timestamp())
        data = self.session.get(uid_url).text  # 请求获取uid
        uid = re.findall(r'"uniqueid":"(.*?)"', data)[0]
        print("成功登陆。\n ")
        return uid

    def cookie(self):
        # TODO
        # https://link.zhihu.com/?target=http%3A//www.lining0806.com/6-%25E7%25BD%2591%25E7%25BB%259C%25E7%2588%25AC%25E8%2599%25AB-%25E9%25AA%258C%25E8%25AF%2581%25E7%25A0%2581%25E7%2599%25BB%25E9%2599%2586/
        # https://link.zhihu.com/?target=https%3A//github.com/lining0806/PythonSpiderNotes/tree/master/ZhihuSpider
        requests_session = requests.session()
        response = requests_session.post(url=url_login, data=data)
        response_captcha = requests_session.get(url=url_login, cookies=cookies)
        response1 = requests.get(url_login)  # 未登陆
        response2 = requests_session.get(
            url_login)  # 已登陆，因为之前拿到了Response Cookie！
        response3 = requests_session.get(
            url_results)  # 已登陆，因为之前拿到了Response Cookie！

    def proxies(self):
        # TODO
        proxies = {}
        response = requests.get(url=url, proxies=proxies)

    def main(self):
        self.post()
