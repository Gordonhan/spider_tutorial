# -*- coding:utf-8 -*-
"""
@author: Gordon Han
@contact: Gordon-Han@hotmail.com
"""
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml.html

from config import *

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.taobao.com/')
        q = wait.until(
            EC.presence_of_element_located((By.ID, "q")))
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.search-button .btn-search")))
        q.send_keys(KEYWORDS)
        submit.click()

        total_page = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.inner .total")))
        parse_page()
        return int(re.search('(\d+)', total_page.text).group(1))
    except TimeoutError:
        return search


def switch_to_page(pagenum):
    try:
        page = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input.input.J_Input')))
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span.btn.J_Submit")))
        page.clear()
        page.send_keys(pagenum)
        submit.click()

        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, 'li.item.active span.num'), str(pagenum)))
        parse_page()
    except TimeoutError:
        switch_to_page(pagenum)


def parse_page():
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    html = browser.page_source
    tree = lxml.html.fromstring(html)
    items = tree.xpath('//div[@class="items"]/div[position()>1]')
    for item in items:
        product = {
            'pic': item.xpath('.//img')[0].get('src'),
            'price': item.xpath('.//div[@class="price g_price g_price-highlight"]/strong')[0].text_content(),
            'deal': item.xpath('.//div[@class="deal-cnt"]')[0].text_content()[0:-3],
            'title': item.xpath('.//a[@class="J_ClickStat"]')[0].text_content().strip(),
            'shop': item.xpath('.//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[position()>1]')[0].text_content(),
            'location': item.xpath('.//div[@class="location"]')[0].text_content(),
        }
        print(product)


def main():
    try:
        total_page = search()
        if total_page:
            for i in range(2, total_page + 1):
                switch_to_page(i)
    finally:
        browser.quit()


if __name__ == '__main__':
    main()
