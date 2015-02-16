# coding:utf-8
'''
Created on 2015年2月16日

@author: chenghao
'''
from lxml import etree
import requests
import json
import codecs


def start():
    re_file = codecs.open("parse_html.json", "wb", encoding="utf-8")
    result = requests.get("http://hao0610.sinaapp.com")
    # 将内容转换为小写, 并转码为utf-8
    page = etree.HTML(result.content.lower().decode('utf-8', 'ignore'))
    # 获取所有 rel='bookmark' 的a标签 
    pages = page.xpath(u"//a[@rel='bookmark']")
    for p in pages:
        # 获取 <a></a>之间的数据, 和href的数据
        line = json.dumps({"name": p.text, "href": p.attrib["href"]}) + "\n"
        re_file.write(line.decode("unicode_escape"))
        
    re_file.close()
    print "完成"
    

start()
