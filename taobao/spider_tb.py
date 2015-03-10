# coding:utf-8
__author__ = 'chenghao'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs
import json
from bs4 import BeautifulSoup
import time
from lxml import etree
from selenium import webdriver
import eventlet
from eventlet import GreenPool

pool = GreenPool()

tb_url = """http://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E8%BF%9E%E8%A1%A3%E8%A3%99+%E5%A4%8F&bcoffset=-3&s="""

headers = {
    'Host': 'www.taobao.com',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',
    'Referer': 's.taobao.com',
}


def demo():
    browser = webdriver.Firefox()

    begin = time.time()
    urls = get_urls()
    for url in urls:
        pool.spawn_n(parse_page, url, browser)
        break

    pool.waitall()
    browser.close()
    # driver.quit()

    print "Elapsed time: %s" % (time.time() - begin)


def parse_page(url, browser):
    browser.get(url)
    content = browser.page_source  # 获取网页源码
    # 将内容转换为小写, 并转码为utf-8
    page = etree.HTML(content.decode('utf-8', 'ignore'))
    #pages = page.xpath("//div[contains(@id, 'J_itemlistCont')]//div[contains(@class, 'item  ')]")
    #for item in pages:
    #    print item.xpath("//div[contains(@class, 'pic-box J_MouseEneterLeave J_PicBox')]//div[contains(@class, 'pic')]//img[contains(@class, 'J_ItemPic img')]/text()")
    items = page.xpath(u"//div[@id='J_itemlistCont']//div[@class='item  ']")
    for item in items:
        item_div = item.xpath(u"div[@class='pic-box J_MouseEneterLeave J_PicBox']//img[@class='J_ItemPic img']")[0].attrib["src"]
        print item_div
        #print etree.tostring(item_div)
        #print item.xpath(u"div[contains(@class, 'pic-box J_MouseEneterLeave J_PicBox')]//div[contains(@class, 'pic')]//img[contains(@class, 'J_ItemPic img')]")
        break

def get_urls():
    urls = []
    for i in xrange(20):  # 0 - 19
        urls.append(tb_url + str(i * 44))
    return urls


demo()
