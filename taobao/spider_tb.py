# coding:utf-8
__author__ = 'chenghao'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import json
import time
from lxml import etree
from selenium import webdriver
from eventlet import GreenPool

pool = GreenPool()
tb_url = """http://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E8%BF%9E%E8%A1%A3%E8%A3%99+%E5%A4%8F&bcoffset=-3&s="""
taobao = codecs.open("taobao.json", "wb", encoding="utf-8")


def demo():
    browser = webdriver.Firefox()

    begin = time.time()
    urls = get_urls()
    for url in urls:
        pool.spawn_n(parse_page, url, browser)

    pool.waitall()
    print "Elapsed time: %s" % (time.time() - begin)
    browser.close()
    taobao.close()


def parse_page(url, browser):
    browser.get(url)
    content = browser.page_source  # 获取网页源码
    # 将内容转换为小写, 并转码为utf-8
    page = etree.HTML(content.decode('utf-8', 'ignore'))
    # lxml中 / 表示下一级元素, // 表示下N级元素(包含下一级元素), 没有 /和// 表示当前元素的下一级元素
    items = page.xpath(u"//div[@id='J_itemlistCont']//div[@class='item  ']")
    for item in items:
        pool.spawn_n(save_data, item)


def save_data(item):
    cover = item.xpath(u"div[@class='pic-box J_MouseEneterLeave J_PicBox']//img")[0].attrib["src"]  # 封面
    title = item.xpath(u"div[@class='pic-box J_MouseEneterLeave J_PicBox']//img")[0].attrib["alt"]  # 商品标题
    url = item.xpath(u"div[@class='pic-box J_MouseEneterLeave J_PicBox']//a")[0].attrib["href"]  # 商品url
    price = item.xpath(u"div[@class='row row-1 g-clearfix']/div[@class='price g_price g_price-highlight']/strong")[0].text  # 商品价格
    deal_num = item.xpath(u"div[@class='row row-1 g-clearfix']/div[@class='deal-cnt']")[0].text
    deal_num = "".join([s for s in deal_num if s.isdigit()])  # 商品购买人数
    shop_url = item.xpath(u"div[@class='row row-3 g-clearfix']//a[@class='shopname J_MouseEneterLeave J_ShopInfo']")[0].attrib["href"]  # 商家url
    shop_name = item.xpath(u"div[@class='row row-3 g-clearfix']//a[@class='shopname J_MouseEneterLeave J_ShopInfo']/span")[1].text  # 商家名称
    location = item.xpath(u"div[@class='row row-3 g-clearfix']/div[@class='location']")[0].text  # 商家地址

    line = json.dumps({
        "cover": cover,
        "title": title,
        "url": url,
        "price": price,
        "deal_num": deal_num,
        "shop_url": shop_url,
        "shop_name": shop_name,
        "location": location
    }) + "\n"
    taobao.write(line.decode("unicode_escape"))


def get_urls():
    urls = []
    for i in xrange(20):  # 0 - 19
        urls.append(tb_url + str(i * 44))
    return urls


demo()
