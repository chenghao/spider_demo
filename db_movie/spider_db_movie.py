# coding:utf-8
'''
Created on 2015年2月15日

@author: chenghao
'''

import requests
import json
import codecs
from bs4 import BeautifulSoup
import threading
import time


headers = { 
            'Host': 'movie.douban.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36',
            'Referer' : 'www.douban.com',
           }

# page_start=0第一页, 1第二页 ......
url = "http://movie.douban.com/j/search_subjects"
url_detail = "http://movie.douban.com/j/subject_abstract?subject_id=%s"

db_movie = codecs.open("db_movie.json", "wb", encoding="utf-8")
db_movie_detail = codecs.open("db_movie_detail.json", "wb", encoding="utf-8")


def demo():
    begin = time.time()
    threads = []
    limit = 10  # 0 - 9
    for i in xrange(limit):
        t = threading.Thread(target=get_movie, name=str(i + 1), args=(url, i))
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
    params = {"type":"movie", "tag":"热门", "sort":"recommend", "page_limit":"20", "page_start":page_start}
    result = requests.get(url, params=params, headers=headers)
    re_content = json.loads(result.content)
    re_data = re_content["subjects"]
    for data in re_data:
        rate = data["rate"]  # 评分
        title = data["title"]  # 电影名
        movie_url = data["url"]
        cover = data["cover"]  # 封面
        movie_id = data["id"]
        
        line = json.dumps({"id":movie_id, "rate":rate, "title":title, "url":movie_url, "cover":cover}) + "\n"
        db_movie.write(line.decode("unicode_escape"))
        
        get_movie_detail(url_detail % movie_id)
        
        
def get_movie_detail(url):
    result = requests.get(url, headers=headers)
    re_content = json.loads(result.content)
    print re_content
    movie_id = re_content["subject"]["id"]
    directors = ",".join(re_content["subject"]["directors"])  # 导演
    duration = re_content["subject"]["duration"] #时长
    actors = ",".join(re_content["subject"]["actors"])  # 演员
    region = re_content["subject"]["region"]  # 地区
    types = ",".join(re_content["subject"]["types"])  # 电影类型
    
    line = json.dumps({"id":movie_id, "directors":directors, "duration":duration, "actors":actors, "region":region, "types":types}) + "\n"
    db_movie_detail.write(line.decode("unicode_escape"))
    
    
demo()
