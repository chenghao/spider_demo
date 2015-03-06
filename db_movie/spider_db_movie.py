# coding:utf-8
'''
Created on 2015年2月15日
@author: chenghao
'''

import requests
import json
import codecs
import threading
import time

import gevent
from gevent.threadpool import ThreadPool
#from eventlet import GreenPool


pool = ThreadPool(20)
#pool = GreenPool(20)
headers = {
    'Host': 'movie.douban.com',
    'User-Agent': '	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Referer': 'www.douban.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Cookie': 'bid="W/D44gE8ksY"; __utma=30149280.1878984429.1423642610.1425614421.1425631983.5; __utmz=30149280.1423642610.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=python%20%B0%B2%D7%B0%20mysqldb; _pk_id.100001.4cf6=ec35457a702f6270.1423992981.3.1425631982.1424050844.; __utma=223695111.716008886.1423992981.1424050029.1425631983.3; __utmz=223695111.1423992981.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118318"; __utmc=30149280; ap=1; _pk_ses.100001.4cf6=*; __utmb=30149280.1.10.1425631983; __utmt_douban=1; __utmb=223695111.0.10.1425631983; __utmc=223695111',
}

url = "http://movie.douban.com/j/search_subjects"
url_detail = "http://movie.douban.com/j/subject_abstract?subject_id=%s"

db_movie = codecs.open("db_movie.json", "wb", encoding="utf-8")
db_movie_detail = codecs.open("db_movie_detail.json", "wb", encoding="utf-8")


def demo():
    begin = time.time()
    #threads = []
    limit = 10  # 0 - 9
    for i in xrange(limit):
        #t = threading.Thread(target=get_movie, name=str(i + 1), args=(url, i * 20))
        #threads.append(t)
        #t.start()

        pool.spawn(get_movie, url, i * 20)

    #pool.waitall()
    gevent.wait()

    #for t in threads:
    #    t.join()

    print "Elapsed time: %s" % (time.time() - begin)

    db_movie.close()
    db_movie_detail.close()

    # get_movie(url, 0)


def get_movie(url, page_start):
    # 搜索热门的电影
    # page_start=0第一页, 20第二页 ......
    params = {"type": "movie", "tag": "热门", "sort": "recommend", "page_limit": "20", "page_start": page_start}
    result = requests.get(url, params=params, headers=headers)
    re_content = json.loads(result.content)
    re_data = re_content["subjects"]
    for data in re_data:
        rate = data["rate"]  # 评分
        title = data["title"]  # 电影名
        movie_url = data["url"]
        cover = data["cover"]  # 封面
        movie_id = data["id"]
        line = json.dumps({"id": movie_id, "rate": rate, "title": title, "url": movie_url, "cover": cover}) + "\n"
        db_movie.write(line.decode("unicode_escape"))
        get_movie_detail(url_detail % movie_id)

        time.sleep(1)


def get_movie_detail(url):
    result = requests.get(url, headers=headers)
    re_content = json.loads(result.content)
    subject = re_content["subject"]

    movie_id = subject["id"]
    directors = ",".join(subject["directors"])  # 导演
    duration = subject["duration"]  # 时长
    actors = ",".join(subject["actors"])  # 演员
    region = subject["region"]  # 地区
    types = ",".join(subject["types"])  # 电影类型
    line = json.dumps({"id": movie_id, "directors": directors, "duration": duration, "actors": actors, "region": region,
                       "types": types}) + "\n"
    db_movie_detail.write(line.decode("unicode_escape"))


demo()
