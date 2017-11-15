# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
import json
import os
from hashlib import md5
import multiprocessing

import re
import requests
import pymongo

from config import *

client = pymongo.MongoClient(MONGODB_URL, connect=False)
db = client[MONGODB_DB]
col = db[MONGODB_COL]


def get_page_index(offset, keyword):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    r = requests.get('https://www.toutiao.com/search_content/', params=params)
    if r.status_code == requests.codes.OK:
        return r.text
    else:
        r.raise_for_status()


def parse_page_index(html):
    result = json.loads(html)
    if result and 'data' in result.keys():
        for item in result.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    document = col.find_one({"_id": url})
    if document:
        print(url, '详情页面已缓存')
        return document['html']
    print('下载详情页面', url)
    r = requests.get(url)
    if r.status_code == requests.codes.OK:
        return r.text
    else:
        r.raise_for_status()


def parse_page_detail(html, url):
    p = re.compile('<title>(.*?)</title>.*?gallery:.(.*?),\n', re.S)
    result = p.search(html)
    if result:
        title = result.group(1)
        data = json.loads(result.group(2))
        if data and 'sub_images' in data.keys():
            image_urls = ['http:' + item.get('url') for item in data.get('sub_images') if 'url' in item.keys()]
            images = list()
            for image_url in image_urls:
                content = download_image(url, image_url)
                images.append({'url': image_url, 'content': content})
                save_image(content, image_url, title)
            return {
                'title': title,
                'html': html,
                'images': images
            }


def save_to_mongodb(url, result):
    if col.update({'_id': url}, {'$set': result}, upsert=True):
        print('存储详情页面到', url)
        return True
    return False


def download_image(url, image_url):
    document = col.find_one({"_id": url})
    if document:
        images = document['images']
        for image in images:
            if image_url == image['url']:
                print(image_url, '图片已缓存')
                return image['content']
    print('下载图片', image_url)
    r = requests.get(image_url)
    if r.status_code == requests.codes.OK:
        return r.content
    else:
        r.raise_for_status()


def save_image(content, url, title):
    file_path = '{0}\\{1}\\{2}.{3}'.format(os.getcwd(), title, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(title):
        os.makedirs(title)
    if not os.path.exists(file_path):
        print('保存图片', url)
        with open(file_path, 'wb') as f:
            f.write(content)
    else:
        print(url, '图片已保存')


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        result = parse_page_detail(html, url)
        if result:
            save_to_mongodb(url, result)


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    groups = [i*10 for i in range(10)]
    pool.map(main, groups)
