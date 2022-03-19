#import tools.login as login
import scrollNclick as browser
import time
#import sys
# sys.path.append('../')


def saveAllSupertopic(start, end, new):
    info = browser.getAllSupertopics(start, end)
    print("saving supertopics")
    browser.saveCSV(info, new, 'SuperTopics.csv', [
                    'SuperTopic', 'Category', 'Id', 'Url', 'Influence', 'Follower'])


def getWeibo(start, end, new):
    info = browser.repostSpider(start, end)
    print("saving weibos")
    browser.saveCSV(info, new, 'Reposts.csv', ['SuperTopic', 'mid', 'uid'])


def main():
    print("Input start: ")
    start = int(input())
    print("Input end: ")
    end = int(input())
    print("Input new: 1 for True, 0 for False")
    new = bool(int(input()))
    saveAllSupertopic(start, end, new)


if __name__ == '__main__':
    main()
