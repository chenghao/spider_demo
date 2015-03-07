# coding:utf-8
__author__ = 'chenghao'

#import requests
import json
import codecs
import threading
import time
from bs4 import BeautifulSoup

#import gevent
#from gevent.threadpool import ThreadPool

import eventlet
from eventlet import GreenPool
requests = eventlet.import_patched("requests")


#pool = ThreadPool(20)
pool = GreenPool(20)

headers = {
    'Host': 'list.iqiyi.com',
    'User-Agent': '	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Referer': 'www.iqiyi.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'QC008=1425443966.1425443966.1425443966.1; QC005=033839b35654de57ca6e94db4226d19a; QC118=%7B%22isFilterImage%22%3A0%2C%22isOpen%22%3A0%2C%22hadTip%22%3A1%7D; jm_1414029808390=1; QC001=1; QC018=; QC911=%2C4%2C; Hm_lvt_53b7374a63c37483e5dd97d78d9bb36e=1425443966; Hm_lpvt_53b7374a63c37483e5dd97d78d9bb36e=1425635366; QC007=DIRECT; QC006=b2slu7u3w6ayyrbjlhvtut7a; T00404=3a4fe70a7536f489b84274b860eff7f3; QC124=0%7C8; QC105=8; QC010=100461277',
}

url = "http://list.iqiyi.com/www/1/-11------------4-%s-1-iqiyi--.html"

iqiyi = codecs.open("iqiyi.json", "wb", encoding="utf-8")


def demo():
    begin = time.time()
    #threads = []
    limit = 30  # 0 - 29
    for i in xrange(limit):
        #t = threading.Thread(target=get_iqiyi, args=(url, i + 1))
        #threads.append(t)
        #t.start()

        pool.spawn(get_iqiyi, url, i + 1)
    #threads = [pool.spawn(get_iqiyi, url, i + 1) for i in xrange(limit)]
    #gevent.joinall(threads)

    pool.waitall()
    #gevent.wait()

    #for t in threads:
    #    t.join()

    print "Elapsed time: %s" % (time.time() - begin)

    iqiyi.close()


def get_iqiyi(url, page_start):
    result = requests.get(url % page_start, headers=headers)
    soup = BeautifulSoup(result.content)
    ul = soup.find_all(class_="site-piclist site-piclist-180236 site-piclist-auto")
    lis = ul[0].find_all("li")

    threads = []
    for li in lis:
        t = threading.Thread(target=save_iqiyi, args=(li, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def save_iqiyi(li):
    img = li.find('img')
    name = img.get("title")
    cover = img.get("src")
    dy_url = li.find(class_="site-piclist_pic_link").get("href").strip()

    line = json.dumps({"name": name, "cover": cover, "dy_url": dy_url}) + "\n"
    iqiyi.write(line.decode("unicode_escape"))


demo()