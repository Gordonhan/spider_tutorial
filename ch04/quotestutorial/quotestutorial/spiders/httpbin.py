# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/post']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, formdata={'name': 'John Doe', 'age': '27'}, callback=self.parse_post, )

    def parse(self, response):
        pass

    def parse_post(self, response):
        self.logger.info(response.text)
