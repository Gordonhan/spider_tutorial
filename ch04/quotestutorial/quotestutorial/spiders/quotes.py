# -*- coding: utf-8 -*-
import scrapy
from quotestutorial.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.col-md-8 .quote')
        for quote in quotes:
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tag::text').extract()

            quotes_item = QuotesItem()
            quotes_item['text'] = text
            quotes_item['author'] = author
            quotes_item['tags'] = tags
            yield quotes_item

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)



