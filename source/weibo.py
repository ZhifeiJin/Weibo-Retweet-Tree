
import supertopic


class Weibo:
    def __init__(self, id = '', user_id = '', user_level = 0, topic_id = -1, content = '', original = True, like_num = 0, ):
        self.id = id
        self.user_id = user_id
        self.user_level = user_level

        self.topic_id = topic_id

        self.content = content
        self.original = original

        self.like_num = like_num
        self.repost_num = repost_num
        self.comment_num = 0
        self.repost_list = []

    def __str__(self):
        """打印一条微博"""
        result = self.content + '\n'
        result += u'微博发布自超话：%s\n' % supertopic.toString(self.topic_id)
        result += u'点赞数：%d\n' % self.like_num
        result += u'转发数：%d\n' % self.retweet_num
        result += u'评论数：%d\n' % self.comment_num
        result += u'url：https://weibo.cn/comment/%s\n' % self.id
        return result
