# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
from urllib import parse

import downloader


def link_crawler(seed_url, scraping_callback, params=None, headers=None, proxies=None, cache=None, delay=1):
    crawl_queue = [seed_url]
    seen = set([seed_url])

    d = downloader.Downloader(headers=headers, proxies=proxies, cache=cache, delay=delay)
    while crawl_queue:
        url = crawl_queue.pop()
        html = d(url, params=params)
        links = scraping_callback(html)
        for link in links:
            link = normalize(seed_url, link)
            if same_domain(seed_url, link) and link not in seen:
                crawl_queue.append(link)
                seen.add(link)


def same_domain(seed_url, url):
    return parse.urlparse(seed_url).netloc == parse.urlparse(url).netloc


def normalize(seed_url, link):
    link, _ = parse.urldefrag(link)
    return parse.urljoin(seed_url, link)
