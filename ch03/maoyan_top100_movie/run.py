# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
import link_crawler
import scraping_callback
import cache

if __name__ == '__main__':
    link_crawler.link_crawler(
        'http://maoyan.com/board/4?offset=0',
        scraping_callback=scraping_callback.scraping_callback,
        headers={'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
        cache=cache.MongoCache(),
        delay=-1
    )
