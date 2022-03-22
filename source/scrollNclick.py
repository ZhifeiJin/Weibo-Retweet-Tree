#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:43:42 2019

@author: chenjianyao

Modified by @ZhifeiJin in August 2020
利用浏览器模拟器来达到滚动、点击、跳转页面的需求
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
import pickle
import functools
import operator
import pandas as pd
import time
from bs4 import BeautifulSoup

username = 'raymondsun97@yahoo.com'  # 微博账号
password = '68458173'  # 微博密码


def init(url="http://weibo.com/login.php"):

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        executable_path="/Users/jinzhifei/anaconda3/lib/python3.7/site-packages/selenium/webdriver/chrome/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-web-security")
    driver.maximize_window()
    driver.get(url)

    time.sleep(45)
    print("结束等待 开始保存cookie")
    # storing the cookies generated by the browser
    cookies = driver.get_cookies()

    # another way to save cookie
    with open('./wb_cookie', 'wb') as f:
        pickle.dump(cookies, f)
    # making a persistent
    params = {'os_username': username, 'os_password': password}
    s = requests.Session()

    # passing the cookies generated from the browser to the session
    c = [s.cookies.set(c['name'], c['value']) for c in cookies]

    resp = s.post(url, params)  # I get a 200 status_code

    # passing the cookie of the response to the browser
    # driver.delete_all_cookies()
    dict_resp_cookies = resp.cookies.get_dict()
    response_cookies_browser = [{'name': name, 'value': value}
                                for name, value in dict_resp_cookies.items()]
    c = [driver.add_cookie(c) for c in response_cookies_browser]
    driver.implicitly_wait(10)     # 等待时间
    return driver
    # the browser now contains the cookies generated from the authentication

    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')    # 不打开浏览器
    # options.add_argument('--disable-gpu')    # 禁用GPU硬件加速
    # options.add_argument(
    # 'user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"')  # 添加访问头
    # options.add_argument('proxy-server="60.13.42.109:9999"')    # 添加代理
    # driver = webdriver.Chrome(options=options)   # 使用驱动配置


def getAllSupertopics(start, end):
    driver = init("https://huati.weibo.cn/discovery/super?suda")
    info = []
    for category in range(start, end):
        cat = []
        try:
            for j in range(20):
                # 第一步：点击第[category]个榜单
                class_list = driver.find_element_by_class_name("superListBox")
                superbox = class_list.find_element_by_id("cate_ul")
                # 第一个榜单是“推荐”，在此不计入。html的element从1开始数
                topic_xpath = "li[position()=" + str(category+1) + "]"
                topic = superbox.find_element_by_xpath(topic_xpath)
                ActionChains(driver).click(topic).perform()
                # 第二步：获取榜单[j]个话题的信息
                # 等待加载
                superarea = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "super_area")))
                step1 = "//*[@class='card-list'][position()={}]".format(j+1)
                element = driver.find_element_by_xpath(step1)
                supertopic = element.find_element_by_class_name("super_name")
                super_name = supertopic.text
                disc = element.find_element_by_class_name("txt-s").text
                influence = parseNumbers(disc.split()[0])
                follower = parseNumbers(disc.split()[1])
                id = category*20 + j
                # 第2.5步：点击超话，获取话题url，返回榜单页面
                supertopic.click()
                redirect = driver.current_url
                topic_url = redirect.split("containerid=")[1].split("&")[0]
                result = [super_name, category, id,
                          topic_url, influence, follower]
                cat.append(result)
                driver.back()
        except Exception as e:
            print(e)
            # if there's an error when crawling one topic, save progress and return
            print("failed with category " + str(category) +
                  ", saving progress and returning.")
            return info
        info.append(cat)
    print("ready to close")
    driver.close()
    driver.quit()
    return info


def parseNumbers(source):
    digits = re.search("[0-9]+", source).group(0)
    unit = re.search("\D", source).group(0)
    if unit == "万":
        n = str(int(digits) * 10000)
    else:
        n = digits
    return n


def saveCSV(l, new, name, header):
    flat = functools.reduce(operator.iconcat, l, [])
    if new:
        print("new")
        with open(name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for i in flat:
                writer.writerow(i)
    else:
        print("not new")
        with open(name, 'a', newline='') as f:
            writer = csv.writer(f)
            for i in flat:
                writer.writerow(i)


def repostSpider(start, end):
    driver = init()
    data = pd.read_csv("SuperTopics.csv")
    references = data["Url"]
    supertopic = data["Id"]
    weibo = []
    # print("总共有%d个超话" % (len(references)))
    for i in range(start, end):
        row = references[i]
        supertopicid = supertopic[i]
        try:
            url = "https://weibo.com/p/{}/super_index".format(row)
            driver.delete_all_cookies()
            time.sleep(2)
            with open('./wb_cookie', 'rb') as f:
                cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
            time.sleep(5)
            driver.get(url)
            try:
                superarea = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "WB_feed")))  # 确认登录超话页面
            except:
                driver.get(url)
            time.sleep(3)
            # print("加载成功 开始滚动")
            page_lst = []
            for page in range(5):
                # 滚动到页面底部
                # print("第%d页，共5页" % (page+1))
                for j in range(5):
                    try:
                        # 如果出现下一页则停止
                        loading = driver.find_element_by_class_name("next")
                        # print("已滚动至页面底部")
                        break
                    except:
                        # 如果出现加载元素则等待
                        try:
                            # print("等待..")
                            loading = driver.find_element_by_class_name(
                                "empty_con")
                            text = loading.find_element_by_class_name("text")
                            # print(text.text)
                            # 如果出现“点击重新载入...”则点击
                            if "加载" not in text.text:
                                # print("点击重新加载")
                                load_again = text.find_element_by_xpath("/a")
                                load_again.click()
                            loading = WebDriverWait(driver, 5).until(
                                EC.invisibility_of_element_located((By.CLASS_NAME, "empty_con")))
                            driver.execute_script(
                                "window.scrollBy(0,document.body.scrollHeight)", "")
                        except:
                            driver.execute_script(
                                "window.scrollBy(0,document.body.scrollHeight)", "")
                            # TODO it should wait some time more or ping and wait
                # print("滚动结束")
                # 确认页面位置
                next = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "next")))
                # 找到当前页面所有微博
                posts = driver.find_elements_by_class_name("WB_feed_like")
                # print("当前有%d条微博" % len(posts))
                if len(posts) < 30:
                    loop = 0
                    while len(posts) < 30 or loop < 5:
                        # print("继续等待...")
                        time.sleep(10)
                        driver.execute_script(
                            "window.scrollBy(0,document.body.scrollHeight)", "")
                        next = WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "next")))
                        posts = driver.find_elements_by_class_name(
                            "WB_feed_like")
                        # print("当前有%d条微博" % len(posts))
                        loop = loop + 1
                for post in posts:
                    uid = post.get_attribute("tbinfo").split("=")[1]
                    mid = post.get_attribute("mid")
                    text1 = post.find_elements_by_class_name(
                        "WB_text")[0].get_attribute('innerHTML')
                    text = BeautifulSoup(text1, 'html.parser').get_text()
                    numbers = post.find_elements_by_class_name('pos')
                    forward = is_int(BeautifulSoup(
                        numbers[1].get_attribute('innerHTML'), "html.parser").get_text()[1:])
                    comment = is_int(BeautifulSoup(
                        numbers[2].get_attribute('innerHTML'), "html.parser").get_text()[1:])
                    like = is_int(BeautifulSoup(
                        numbers[3].get_attribute('innerHTML'), "html.parser").get_text()[1:])
                    p = [supertopicid, uid, mid, text, forward, comment, like]
                    page_lst.append(p)
                if page < 4:
                    next.click()
                    time.sleep(10)
            weibo.append(page_lst)
            # print("本超话结束")
        except Exception as e:
            # if there's an error when crawling one topic, save progress and return
            print("failed with row " + str(i) +
                  ", skipping to next supertopic.")
            continue
    return weibo


def is_int(s):
    '''s is a string. returns s as an int if s is an integer, 0 otherwise.'''
    try:
        if int(s) > 0:
            return int(s)
    except:
        return 0


def base62_encode(num):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)