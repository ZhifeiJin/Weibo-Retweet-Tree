'''
用于处理微博登录问题
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
    def __init__(self, username, password, link):
        self.username = 'raymondsun97@yahoo.com'
        self.password = '68458173'
        self.session = requests.session()  # 登录用session
        #self.link = link
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.session.verify = False  # 取消证书验证

    def prelogin(self):
        '''预登录，获取一些必须的参数'''
        self.su = base64.b64encode(
            self.username.encode())  # 阅读js得知用户名进行base64转码
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_={}'.format(
            quote(self.su), get_timestamp())  # 注意su要进行quote转码
        response = self.session.get(url).content.decode()
        # print(response)
        self.nonce = re.findall(r'"nonce":"(.*?)"', response)[0]
        self.pubkey = re.findall(r'"pubkey":"(.*?)"', response)[0]
        self.rsakv = re.findall(r'"rsakv":"(.*?)"', response)[0]
        self.servertime = re.findall(r'"servertime":(.*?),', response)[0]
        return self.nonce, self.pubkey, self.rsakv, self.servertime

    def get_sp(self):
        '''用rsa对明文密码进行加密，加密规则通过阅读js代码得知'''
        publickey = rsa.PublicKey(int(self.pubkey, 16), int('10001', 16))
        message = str(self.servertime) + '\t' + \
            str(self.nonce) + '\n' + str(self.password)
        self.sp = rsa.encrypt(message.encode(), publickey)
        return b2a_hex(self.sp)

    def login(self):
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
            'sp': self.get_sp(),
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
        print(result)
        print(re.findall(r'ticket=(.*?)&ssosavestate=(.*?)"', result))
        ticket, ssosavestate = re.findall(
            r'ticket=(.*?)&ssosavestate=(.*?)"', result)[0]  # 获取ticket和ssosavestate参数
        uid_url = 'https://passport.weibo.com/wbsso/login?ticket={}&ssosavestate={}&callback=sinaSSOController.doCrossDomainCallBack&scriptId=ssoscript0&client=ssologin.js(v1.4.19)&_={}'.format(
            ticket, ssosavestate, get_timestamp())
        data = self.session.get(uid_url).text  # 请求获取uid
        uid = re.findall(r'"uniqueid":"(.*?)"', data)[0]
        print("uid is " + uid)
        return uid

    def getlink(self):
        html = self.session.get(self.link)
        f = open("list.html", "wb")
        f.write(html.text.encode())
        f.close()
        f = open("list.html", "rb")
        data = f.read()
        f.close()
        pattern = '\"text\": \".*?,'
        data = re.compile(pattern).findall(str(data))
        print(data)
        pattern = "href=.*?data"
        data = re.compile(pattern).findall(str(data))

        link = []
        for i in data:
            pattern = 'https://.*?\"'
            url = re.compile(pattern).findall(i)
            link += url
        return link

    def getAllSuperTopics(self, link, uid):
        url = "https://huati.weibo.cn/discovery/super?suda"
        topics = ["明星", "饭圈", "CP", "游戏", "动漫", "综艺", "电视剧", "地区", "音乐", "时尚美妆", "读书", "情感", "颜值", "体育", "运动健身", "曲艺", "秀场", "工艺", "摄影", "萌宠", "闲趣", "美食",
                  "互联网", "好好学习", "艺术", "设计美学", "舞蹈", "旅游", "校园", "搞笑幽默", "行业", "财经", "家居", "育儿", "医疗", "养生", "数码", "汽车", "科普", "军事", "历史", "宗教", "收藏", "房产", "航空"]
        for i in topics:
            try:
                html = self.session.get(i)

                time.sleep(40)

            except:
                print("Error: Failed when getting url from SuperTopic " + i + "\n")
                pass

    def main(self):
        self.prelogin()
        self.get_sp()
        uid = self.login()
        link = self.getlink()
        #self.complain(link, uid)


if __name__ == '__main__':
    username = 'raymondsun97@yahoo.com'  # 微博账号
    password = ''  # 微博密码
    #link = "https://huati.weibo.cn/discovery/super?suda"
    sess = LogIn(username, password, link)
    sess.main()
