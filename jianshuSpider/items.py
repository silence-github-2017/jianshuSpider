# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuspiderItem(scrapy.Item):
    """
    title = response.xpath("//h1[@class='title']/text()").get()
    author = response.xpath("//span[@class='name']/a/text()").get()
    avator = response.xpath("//a[@class='avatar']/img/@src").get()
    # 文章html内容
    content_html = response.xpath("div[@class='show-content-free']").get()
    # 发布时间
    p_time = response.xpath("//span[@class='publish-time']/text()").get().replace('*','')
    # 文章id
    article_id = response.url.split("?")[0].split('/')[-1]
    # 文章链接
    link_url = response.url
    """
    title = scrapy.Field()
    author = scrapy.Field()
    avator = scrapy.Field()
    content_html = scrapy.Field()
    p_time = scrapy.Field()
    article_id = scrapy.Field()
    link_url = scrapy.Field()
