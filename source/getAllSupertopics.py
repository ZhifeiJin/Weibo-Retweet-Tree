"""
获取所有超话榜单(45个)中前100个超话的信息，包括所在榜单id，超话名，影响力值，粉丝数，榜单排名，阅读数，帖子数。
把以上数据存为csv格式。
"""
import tools.login as login
import tools.scrollNclick as browser
import csv
#import sys
# sys.path.append('../')
url = "https://huati.weibo.cn/discovery/super?suda"
topics = ["明星", "饭圈", "CP", "游戏", "动漫", "综艺", "电视剧", "地区", "音乐", "时尚美妆", "读书", "情感", "颜值", "体育", "运动健身", "曲艺", "秀场", "工艺", "摄影", "萌宠", "闲趣", "美食",
          "互联网", "好好学习", "艺术", "设计美学", "舞蹈", "旅游", "校园", "搞笑幽默", "行业", "财经", "家居", "育儿", "医疗", "养生", "数码", "汽车", "科普", "军事", "历史", "宗教", "收藏", "房产", "航空"]


def testLogIn():
    session = login.LogIn()
    session.main()


def testbrowser():
    session = login.LogIn()
    session.main()
    browser.init()
    #result = browser.isPresent()
    #print('判断页面1成功 0失败  结果是=%d' % result)


def main():
    testbrowser()


if __name__ == '__main__':
    main()
