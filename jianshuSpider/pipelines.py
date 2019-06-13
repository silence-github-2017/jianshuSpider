# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

class JianshuspiderPipeline(object):
    def __init__(self):
        db_param = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'yp@520',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.connect = pymysql.connect(**db_param)
        self.cursor = self.connect.cursor()
        self.__sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['author'], item['avator'],
                            item['content_html'], item['p_time'], item['article_id'],
                                       item['link_url']))
        self.connect.commit()
        return item

    @property
    def sql(self):
        if self.__sql is None:
            self.__sql = """
             insert into article (id, title,author,avator,content_html,p_time,article_id,link_url)
             VALUE (null, %s,%s,%s,%s,%s,%s,%s)
            """
        else:
            return self.__sql


class JianshuTwistedPipeline(object):
    def __init__(self):
        db_param = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'yp@520',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.adbapi = adbapi.ConnectionPool('pymysql',**db_param)
        self.__sql = None

    @property
    def sql(self):
        if self.__sql is None:
            self.__sql = """
                 insert into article_copy (id, title,author,avator,content_html,p_time,article_id,link_url,
                 views_count,comments_count,likes_count)
                 VALUE (null, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        else:
            return self.__sql

    def process_item(self, item, spider):
        # 将同步转化为异步处理
        defer = self.adbapi.runInteraction(self.insert_item, item)
        defer.addErrback(self.handler_error, item, spider)
        return item

    # 注意cursor 必须放到第一个位置
    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['author'], item['avator'],
        item['content_html'], item['p_time'], item['article_id'],
        item['link_url'],item['views_count'],item['comments_count'], item['likes_count']))

    def handler_error(self, error, item, spider):
        print("---------"+str(error)+"-------------")


