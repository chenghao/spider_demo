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


headers = {
    'Host': 'movie.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36',
    'Referer': 'www.douban.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Cookie': 'bid="t+vhk8fr4C8"; ap=1; ll="118318"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1424048779%2C%22http%3A%2F%2Fwww.tuicool.com%2Farticles%2FB3yU32j%22%5D; _pk_id.100001.4cf6=01f40bbbf01eff44.1423900418.4.1424048779.1423993192.; __utma=30149280.596929389.1423643421.1423991649.1424048779.5; __utmc=30149280; __utmz=30149280.1423991649.4.4.utmcsr=tuicool.com|utmccn=(referral)|utmcmd=referral|utmcct=/articles/B3yU32j; __utma=223695111.634150975.1423900418.1423991649.1424048779.4; __utmc=223695111; __utmz=223695111.1423991649.3.3.utmcsr=tuicool.com|utmccn=(referral)|utmcmd=referral|utmcct=/articles/B3yU32j',
}

url = "http://movie.douban.com/j/search_subjects"
url_detail = "http://movie.douban.com/j/subject_abstract?subject_id=%s"

db_movie = codecs.open("db_movie.json", "wb", encoding="utf-8")
db_movie_detail = codecs.open("db_movie_detail.json", "wb", encoding="utf-8")
lock = threading.Lock()


def demo():
    begin = time.time()
    threads = []
    limit = 10  # 0 - 9
    for i in xrange(limit):
        t = threading.Thread(target=get_movie, name=str(i + 1), args=(url, i * 20))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

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
        # lock.acquire()
        line = json.dumps({"id": movie_id, "rate": rate, "title": title, "url": movie_url, "cover": cover}) + "\n"
        db_movie.write(line.decode("unicode_escape"))
        # lock.release()
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
    # lock.acquire()
    line = json.dumps({"id": movie_id, "directors": directors, "duration": duration, "actors": actors, "region": region,
                       "types": types}) + "\n"
    db_movie_detail.write(line.decode("unicode_escape"))
    # lock.release()


demo()
