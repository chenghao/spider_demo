# coding:utf-8
__author__ = 'chenghao'

import requests
import codecs
import json
from bs4 import BeautifulSoup
import threading
import time
from selenium import webdriver

tb_url = """http://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E8%BF%9E%E8%A1%A3%E8%A3%99+%E5%A4%8F&bcoffset=-3&s="""

headers = {
    'Host': 'www.taobao.com',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',
    'Referer': 's.taobao.com',
}


def demo():
    begin = time.time()
    threads = []
    urls = get_urls()
    driver = webdriver.Firefox()
    for url in urls:
        '''
        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content)
        print soup
        print soup.find_all(class_="pic-box-inner")
        '''
        driver.get(url)
        print driver
        #comment = driver.find_element_by_xpath("//div[contains(@id, 'mainsrp-itemlist')]//div[contains(@class, 'item')]")
        comments = driver.find_elements_by_css_selector("div#mainsrp-itemlist div.item")
        for item in comments:
            print item.text
            print "....................................................."
            #print item.find_element_by_xpath("//div[contains(@class, 'pic-box-inner')]//a[contains(@class, 'pic-link J_U2IStat J_ItemPicA')]//img[contains(@class, 'J_ItemPic img')]").get_attribute("src")
        break

    driver.close()
    # driver.quit()

    for t in threads:
        t.join()

    print "Elapsed time: %s" % (time.time() - begin)


def get_urls():
    urls = []
    for i in xrange(20):  # 0 - 19
        urls.append(tb_url + str(i * 44))
    return urls


demo()
