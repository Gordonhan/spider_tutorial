# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
import re
import csv
import json
import multiprocessing

import requests

lock = multiprocessing.Lock()

def get_page(offset):
    params = {'offset': offset}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    r = requests.get('http://maoyan.com/board/4', params=params, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        r.raise_for_status()


def parse_page(html):
    p = re.compile('<dd>.*?<i.*?board-index.*?>(\d+)</i>.*?<img.*?<img.*?'
                   + 'src="(.*?)".*?<p.*?<a.*?>(.*?)</a>.*?<p.*?>(.*?)</p>.*?'
                   + '<p.*?>(.*?)</p>.*?<i.*?>(.*?)</i>.*?<i.*?>(.*?)</i>',
                   re.S)
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

    # with open('maoyan.csv', 'a', encoding='utf-8') as f:
    #     w = csv.writer(f)
    #     w.writerow(['index', 'img', 'title', 'star', 'time', 'score'])
    #     lock.acquire()
    #     for result in p.findall(html):
    #         w.writerow([result[0], result[1], result[2], result[3].strip()[3:], result[4].strip()[5:], result[5] + result[6]])
    #     lock.release()
    #


def main(offset):
    html = get_page(offset)
    parse_page(html)


if __name__ == '__main__':
    groups = [i*10 for i in range(10)]
    pool = multiprocessing.Pool()
    pool.map(main, groups)
