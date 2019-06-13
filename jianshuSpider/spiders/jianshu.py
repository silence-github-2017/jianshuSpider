# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshuSpider.items import JianshuspiderItem


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']
    # https://www.jianshu.com/p/864acea4eda4
    # https://www.jianshu.com/p/eee9afc9486c?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_item(self, response):
        pass

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        author = response.xpath("//span[@class='name']/a/text()").get()
        avator = response.xpath("//a[@class='avatar']/img/@src").get()
        # 文章html内容
        content_html = response.xpath("//div[@class='show-content']").get()
        # 发布时间
        p_time = response.xpath("//span[@class='publish-time']/text()").get().replace('*', '')
        # 文章id
        article_id = response.url.split("?")[0].split('/')[-1]
        # 文章链接
        link_url = response.url
        # 喜欢数
        likes_count = response.xpath("//span[@class='likes-count']/text()").get()
        # 评论
        comments_count = response.xpath("//span[@class='comments-count']/text()").get()
        # 阅读量
        views_count = response.xpath("//span[@class='views-count']/text()").get()
        items = JianshuspiderItem(
            title=title,
            author=author,
            avator=avator,
            content_html=content_html,
            p_time=p_time,
            article_id=article_id,
            link_url=link_url,
            likes_count=likes_count,
            comments_count=comments_count,
            views_count=views_count
        )
        yield items
