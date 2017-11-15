# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
import re
import json

import lxml.html

import config


def scraping_callback(html):
    scraping(html)
    return get_follow_pages(html)


def scraping(html):
    p = re.compile('<dd>.*?<i.*?board-index.*?>(\d+)</i>.*?<img.*?<img.*?'
                   + 'src="(.*?)".*?<p.*?<a.*?>(.*?)</a>.*?<p.*?>(.*?)</p>.*?'
                   + '<p.*?>(.*?)</p>.*?<i.*?>(.*?)</i>.*?<i.*?>(.*?)</i>', re.S)
    with open('MaoYan.txt', 'a', encoding='utf-8') as f:
        for result in p.findall(html):
            r = {
                "index": result[0],
                "img": result[1],
                "title": result[2],
                "star": result[3].strip()[3:],
                "time": result[4].strip()[5:],
                "score": result[5] + result[6]
            }
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def get_follow_pages(html):
    tree = lxml.html.fromstring(html)
    links = tree.xpath('//ul[@class="list-pager"]/li[last()]/a')
    for link in links:
        yield link.get('href')


def match(link, link_regex):
    return re.match(link_regex, link)


def get_links(html):
    web_page = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return web_page.findall(html)
