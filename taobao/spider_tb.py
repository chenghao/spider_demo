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
    for url in urls:
        '''
        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content)
        print soup
        print soup.find_all(class_="pic-box-inner")
        '''
        c = webdriver.Firefox()
        c.get(url)
        comment = c.find_element_by_id('media_comment')
        count = comment.find_element_by_class_name('f_red')
        print count.text
        break
    for t in threads:
        t.join()

    print "Elapsed time: %s" % (time.time() - begin)


def get_urls():
    urls = []
    for i in xrange(20):  # 0 - 19
        urls.append(tb_url + str(i * 44))
    return urls


demo()
