# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
import requests
from urllib import parse
from datetime import datetime
import time


class Downloader:
    def __init__(self, headers=None, proxies=None, cache=None, delay=1):
        self.headers = headers
        self.proxies = proxies
        self.cache = cache
        self.throttle = Throttle(delay)

    def __call__(self, url, params=None):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
                print(url, "is cached")
            except KeyError:
                pass
        if result is None:
            self.throttle.wait(url)
            result = self.download(url, params=params)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, params=None):
        print('downloading', url)
        r = requests.get(url, params=params, headers=self.headers, proxies=self.proxies)
        if r.status_code == requests.codes.OK:
            return {'html': decode_content(r), 'code': r.status_code}
        else:
            print('download fail')
            r.raise_for_status()


class Throttle(object):
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_time = self.delay\
                         - (datetime.now() - last_accessed).seconds
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.domains[domain] = datetime.now()


def decode_content(r):
    encoding = r.encoding
    if encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(r.text)
        encoding = encodings[0] if encodings else r.apparent_encoding
    return r.content.decode(encoding, 'replace')
