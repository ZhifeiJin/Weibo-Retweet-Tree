#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:43:42 2019

@author: chenjianyao

Modified by @ZhifeiJin in August 2020
利用浏览器模拟器来达到滚动、点击、跳转页面的需求
"""
import time
import xlrd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
#import excelSave as save
import tools.login


def init():
    options = Options()
    options.add_argument('--headless')    # 不打开浏览器
    options.add_argument('--disable-gpu')    # 禁用GPU硬件加速
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"')  # 添加访问头
    # options.add_argument('proxy-server="60.13.42.109:9999"')    # 添加代理
    driver = webdriver.Chrome(options=options)   # 使用驱动配置
    driver.get("https://huati.weibo.cn/discovery/super?suda")
    driver.implicitly_wait(10)     # 等待时间
    element = driver.find_element_by_xpath(
        "//div[@id='cssready']")    # 执行页面定位语句
    isDisplayed = element.is_displayed()   # 判断是否允许访问
    print(isDisplayed)
    print(element.text)

    # 将滚动条移动到页面的顶部 0：为顶部；1000000：为底部
    js = "var q=document.documentElement.scrollTop=10000000000"    # js语句
    driver.execute_script(js)    # 执行语句

    driver.close()


"""
用来控制页面滚动
"""


def Transfer_Clicks(browser):
    try:
        browser.execute_script(
            "window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"


"""判断页面是否加载出来"""


def isPresent():
    temp = 1
    try:
        driver.find_elements_by_css_selector(
            'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
    except:
        temp = 0
    return temp

# 把超话页面滚动到底


def SuperwordRollToTheEnd():
    before = 0
    after = 0
    n = 0
    timeToSleep = 50
    while True:
        before = after
        Transfer_Clicks(driver)
        time.sleep(3)
        elems = driver.find_elements_by_css_selector('div.m-box')
        print("当前包含超话最大数量:%d,n当前的值为:%d,当n为5无法解析出新的超话" % (len(elems), n))
        after = len(elems)
        if after > before:
            n = 0
        if after == before:
            n = n + 1
        if n == 5:
            print("当前包含最大超话数为：%d" % after)
            break
        if after > timeToSleep:
            print("抓取到%d多条超话，休眠30秒" % timeToSleep)
            timeToSleep = timeToSleep + 50
            time.sleep(30)
# 插入数据


def insert_data(elems, path, name, yuedu, taolun):
    for elem in elems:
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        rid = rows_old
        # 用户名
        weibo_username = elem.find_elements_by_css_selector(
            'h3.m-text-cut')[0].text
        weibo_userlevel = "普通用户"
        # 微博等级
        try:
            weibo_userlevel_color_class = elem.find_elements_by_css_selector(
                "i.m-icon")[0].get_attribute("class").replace("m-icon ", "")
            if weibo_userlevel_color_class == "m-icon-yellowv":
                weibo_userlevel = "黄v"
            if weibo_userlevel_color_class == "m-icon-bluev":
                weibo_userlevel = "蓝v"
            if weibo_userlevel_color_class == "m-icon-goldv-static":
                weibo_userlevel = "金v"
            if weibo_userlevel_color_class == "m-icon-club":
                weibo_userlevel = "微博达人"
        except:
            weibo_userlevel = "普通用户"
        # 微博内容
        weibo_content = elem.find_elements_by_css_selector(
            'div.weibo-text')[0].text
        shares = elem.find_elements_by_css_selector(
            'i.m-font.m-font-forward + h4')[0].text
        comments = elem.find_elements_by_css_selector(
            'i.m-font.m-font-comment + h4')[0].text
        likes = elem.find_elements_by_css_selector(
            'i.m-icon.m-icon-like + h4')[0].text
        # 发布时间
        weibo_time = elem.find_elements_by_css_selector('span.time')[0].text
        print("用户名：" + weibo_username + "|"
              "微博等级：" + weibo_userlevel + "|"
              "微博内容：" + weibo_content + "|"
              "转发：" + shares + "|"
              "评论数：" + comments + "|"
              "点赞数：" + likes + "|"
              "发布时间：" + weibo_time + "|"
              "话题名称" + name + "|"
              "话题讨论数" + yuedu + "|"
              "话题阅读数" + taolun)
        value1 = [[rid, weibo_username, weibo_userlevel, weibo_content,
                   shares, comments, likes, weibo_time, keyword, name, yuedu, taolun], ]
        print("当前插入第%d条数据" % rid)
        save.write_excel_xls_append_norepeat(book_name_xls, value1)
# 获取当前页面的数据


def get_current_weibo_data(elems, book_name_xls, name, yuedu, taolun, maxWeibo):
    # 开始爬取数据
    before = 0
    after = 0
    n = 0
    timeToSleep = 100
    while True:
        before = after
        Transfer_Clicks(driver)
        time.sleep(3)
        elems = driver.find_elements_by_css_selector('div.card.m-panel.card9')
        print("当前包含微博最大数量：%d,n当前的值为：%d, n值到5说明已无法解析出新的微博" % (len(elems), n))
        after = len(elems)
        if after > before:
            n = 0
        if after == before:
            n = n + 1
        if n == 5:
            print("当前关键词最大微博数为：%d" % after)
            insert_data(elems, book_name_xls, name, yuedu, taolun)
            break
        if len(elems) > maxWeibo:
            print("当前微博数以达到%d条" % maxWeibo)
            insert_data(elems, book_name_xls, name, yuedu, taolun)
            break
        if after > timeToSleep:
            print("抓取到%d多条，插入当前新抓取数据并休眠30秒" % timeToSleep)
            timeToSleep = timeToSleep + 100
            insert_data(elems, book_name_xls, name, yuedu, taolun)
            time.sleep(30)
# 点击超话按钮，获取超话页面


def get_superWords():
    time.sleep(5)
    elem = driver.find_element_by_xpath(
        "//*[@class='scroll-box nav_item']/ul/li/span[text()='话题']")
    elem.click()
    # 获取所有超话
    SuperwordRollToTheEnd()
    elemsOfSuper = driver.find_elements_by_css_selector(
        'div.card.m-panel.card26')
    return elemsOfSuper


def get_superwordUrl():
    elemsOfSuper = get_superWords()
    superWords_url = []
    for i in range(0, len(elemsOfSuper)):
        print("当前获取第%d个超话链接，共有%d个超话" % (i+1, len(elemsOfSuper)))
        time.sleep(1)
        element = driver.find_elements_by_css_selector(
            'div.card.m-panel.card26')[i]
        # 获取话题名称，话题讨论书，阅读数
        driver.execute_script('arguments[0].click()', element)
        time.sleep(3)
        print(driver.current_url)
        superWords_url.append(driver.current_url)
        driver.back()
    return superWords_url
# 爬虫运行


def spider(username, password, driver, book_name_xls, sheet_name_xls, keyword, maxWeibo):
    # 加载驱动，使用浏览器打开指定网址
    driver.set_window_size(452, 790)
    driver.get(
        "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F")
    time.sleep(3)
    # 登陆
    elem = driver.find_element_by_xpath("//*[@id='loginName']")
    elem.send_keys(username)
    elem = driver.find_element_by_xpath("//*[@id='loginPassword']")
    elem.send_keys(password)
    elem = driver.find_element_by_xpath("//*[@id='loginAction']")
    elem.send_keys(Keys.ENTER)
    # 判断页面是否加载出
    while 1:  # 循环条件为1必定成立
        result = isPresent()
        print('判断页面1成功 0失败  结果是=%d' % result)
        if result == 1:
            elems = driver.find_elements_by_css_selector(
                'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
            # return elems #如果封装函数，返回页面
            break
        else:
            print('页面还没加载出来呢')
            time.sleep(20)
    time.sleep(5)
    # 搜索关键词
    elem = driver.find_element_by_xpath("//*[@class='m-text-cut']").click()
    time.sleep(5)
    elem = driver.find_element_by_xpath("//*[@type='search']")
    elem.send_keys(keyword)
    elem.send_keys(Keys.ENTER)

    superWords_url = get_superwordUrl()
    print("超话链接获取完毕，休眠60秒")
    time.sleep(60)
    for url in superWords_url:
        driver.get(url)
        time.sleep(3)
        name = driver.find_element_by_xpath(
            "//*[@class='m-box-col m-box-dir npg-desc']/h4[@class='m-text-cut firsth']").text.replace("热搜", "").replace("\n", "")
        yuedu_taolun = driver.find_element_by_xpath(
            "//*[@class='m-box-col m-box-dir npg-desc']/h4[@class='m-text-cut']").text
        yuedu = yuedu_taolun.split(" ")[0]
        taolun = yuedu_taolun.split(" ")[1]
        time.sleep(5)
        get_current_weibo_data(elems, book_name_xls, name,
                               yuedu, taolun, maxWeibo)  # 爬取综合
        time.sleep(3)
        shishi_element = driver.find_element_by_xpath(
            "//*[@class='scroll-box nav_item']/ul/li/span[text()='实时']")
        driver.execute_script('arguments[0].click()', shishi_element)
        get_current_weibo_data(elems, book_name_xls, name,
                               yuedu, taolun, maxWeibo)  # 爬取实时
        time.sleep(5)
        remen_element = driver.find_element_by_xpath(
            "//*[@class='scroll-box nav_item']/ul/li/span[text()='热门']")
        driver.execute_script('arguments[0].click()', remen_element)
        get_current_weibo_data(elems, book_name_xls, name,
                               yuedu, taolun, maxWeibo)  # 爬取热门


if __name__ == '__main__':
    # username = ""  # 你的微博登录名
    # password = ""  # 你的密码
    driver = webdriver.Chrome(
        '/Users/Desktop/Weibo-Retweet-Tree/chromedriver')
    # book_name_csv = "/Users/Desktop/AllSuperTopics.csv"  # 填写你想存放excel的路径，没有文件会自动创建
    # sheet_name_xls = 'all'  # sheet表名
    # maxWeibo = 1000  # 设置最多多少条微博，如果未达到最大微博数量可以爬取当前已解析的微博数量

    for i in topics:
        try:
            username = 'raymondsun97@yahoo.com'  # 微博账号
            password = '68458173'  # 微博密码
            sess = LogIn(username, password, link)
            html = sess.session.get(url)
            spider(driver, book_name_xls,
                   sheet_name_xls, keyword, maxWeibo)
            time.sleep(40)

        except:
            print("Error: Failed when getting url from SuperTopic " + i + "\n")
            pass  # 输入你想要的关键字，可以是多个关键词的列表的形式
