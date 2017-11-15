# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
from urllib.parse import urlencode
from time import sleep

import requests

KEYWORD = '风景'

headers = {
    'Cookie':'IPLOC=CN4406; SUID=572E1BB72F20910A0000000059B717B2; SUV=1509950709549883; pgv_pvi=8479528960; ABTEST=6|1509952004|v1; weixinIndexVisited=1; SUIR=D1147246383D6A7DCAC8993338230CED; pgv_si=s8080480256; JSESSIONID=aaaJDiwZDxYCOak9tBv8v; ppinf=5|1510113232|1511322832|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMjpNci4lRTklOUYlQTl8Y3J0OjEwOjE1MTAxMTMyMzJ8cmVmbmljazoxMjpNci4lRTklOUYlQTl8dXNlcmlkOjQ0Om85dDJsdU1DaW5iR1lPazV0NV95emhhNDBlSm9Ad2VpeGluLnNvaHUuY29tfA; pprdig=OGVs3YDBLK1Dqt-JFuyj5p4Jy0KPQa-5jIaVgT6JUH1NUAgaitFmbITWe9mzPO77QrC3bRzulBIi9nb7wsz5tzlh_L6fChEiNrDRg-cxWiJq57okVNPgxfOzcFrTSjkZA5eizJEr8UJwDY24bBldNfJCFlm1wGMnGy6uuDgkdRU; sgid=14-31810969-AVoCf9CPG3NHom8z4sqFYdk; PHPSESSID=hpi1qdaheqk65v785rp6ot1ag1; sct=12; ld=ekllllllll2zllPxlllllVojhT9llllltUU0ikllllwllllljllll5@@@@@@@@@@; LSTMV=288%2C155; LCLKINT=10578; ssuid=7440072057; dt_ssuid=7013969325; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ppmdig=1510132696000000d77da20624d604414e3a1b9982f39600; SNUID=754E2B1E6E6B321B0396825A6F4792E1; seccodeRight=success; successCount=1|Wed, 08 Nov 2017 09:42:00 GMT',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

proxies = None


def set_proxies():
    global proxies
    try:
        r = requests.get('http://localhost:5000/get')
    except ConnectionError:
        proxies = None
    else:
        if r.status_code == 200:
            proxies = {
                'http': 'http://' + r.text
            }
        else:
            proxies = None


def get_html(url):
    print('useing', proxies['http'] if proxies else 'localhost')
    print('downloading', url)
    try:
        r = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False)
        if r.status_code == 200:
            print('download successed')
            return r.text
        elif r.status_code == 302:
            print('need proxy')
            set_proxies()
            if proxies:
                print('set proxy successed')
                return get_html(url)
            else:
                print('set proxy failed')
                return None
        else:
            print('otther http status code', r.status_code)
            return None
    except ConnectionError:
        print('download', url, 'failed')
        return None
    except requests.exceptions.ProxyError:
        print('bad proxy', proxies['http'])
        set_proxies()
        if proxies:
            print('set proxy successed')
            return get_html(url)
        else:
            print('set proxy failed')
            return None


def get_page_index(page):
    global proxies
    query = {
        'query': KEYWORD,
        'type': 2,
        'page': page
    }
    url = 'http://weixin.sogou.com/weixin?' + urlencode(query)
    return get_html(url)


def main():
    for i in range(1, 101):
        html = get_page_index(i)
        if html:
            print(html)


if __name__ == '__main__':
    main()
