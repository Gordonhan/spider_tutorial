# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from zhihuuser.items import UserItem



class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followees_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(url=self.user_url.format(user=self.start_user, include=self.user_include), callback=self.parse_user)
        yield Request(url=self.followees_url.format(user=self.start_user, include=self.followees_include, offset=0, limit=20), callback=self.parse_followees)
        yield Request(url=self.followers_url.format(user=self.start_user, include=self.followers_include, offset=0, limit=20), callback=self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

    def parse_followees(self, response):
        result = json.loads(response.text)
        if 'data' in result.keys():
            for data in result.get('data'):
                yield Request(url=self.user_url.format(user=data.get('url_token'), include=self.user_include), callback=self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end') is False:
            next_page = result.get('paging').get('next')
            yield Request(url=next_page, callback=self.parse_followees)

    def parse_followers(self, response):
        result = json.loads(response.text)
        if 'data' in result.keys():
            for data in result.get('data'):
                yield Request(url=self.user_url.format(user=data.get('url_token'), include=self.user_include), callback=self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end') is False:
            next_page = result.get('paging').get('next')
            yield Request(url=next_page, callback=self.parse_followers)

