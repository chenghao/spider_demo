# coding:utf-8
'''
Created on 2015年2月15日

@author: chenghao
'''
import json
import codecs
from bs4 import BeautifulSoup
import time
import eventlet
from eventlet import GreenPool
requests = eventlet.import_patched("requests")

pool = GreenPool(200)
headers = {
    # 登录后的Cookie
    'Cookie': 'advertisement_id=2104; advertisement_skey=%C6%B7%D7%A8%B1%EA%CC%E2; visitid_time=2015-1-27%209%3A44%3A32; hcbrowserid=C6791BD6058000016F3E11A91C053470; hcsearch=2015012709465530362.89150099; PHPStat_HC360_First_Time_aejmffgh=1422324267091; PHPStat_HC360_Cookie_Global_User_Id=_ck15012710042710989484515874565; PHPStat_HC360_Return_Time_aejmffgh=1422324267091; Hm_lvt_4fea1a6421a72296a12cd7898b93858e=1422324268; notehccomm_id=2015012710085913638950; search_key=""; LoginID=chenghao0610; pubbusinhelp=1; user-key=C243828BDA900001117814821699D620; hckIndex=C24380B01AA00001FE7F1AB01DC56000%231%23hc360.com%232%23viewwords1%232%2331535999999; contactViewCount=1; Hm_lvt_c1bfff064e4a03c5b6f2b589e099da36=1422325305; hccordet=00; hcpreurl=; __utma=58102070.1870460405.1422324714.1422428449.1422437654.11; __utmc=58102070; __utmz=58102070.1422324714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=0000Zv6F-8b5JgPd0RwL9-ZLqVz:16s8qjjcb; hc360analyid=C686B33D92400001711CCEDCBB1BCDD0; hc360analycopyid=C686B33D925000017491117071E9CE80; hcvisittag=chenghao0610#0#34#567#0#1; HC360.SSOUser=0cda74b9dce2afb9199670b623790c146fabcc044b7caa63d52a78b848b7961a142d6f969bf3d048546ac0b6a9290dba76263ca8c5a7847f7317ff57670b5848e2b3f4b062ea18cf9ecba198d63911c719fcc8e5645c4795fea427fd0c77f4c48c0884d137acbfa90c5a979bd9f077d19f9ac5d331bb2a749fd9162294cf2b15879698c00de76cd8; loginTime="2015-03-10 15:14:27"; lastloginusers=chenghao0610; LoginID4System=42109723; urgeStay=1; hc360_userid=42109723; hc360visitid=C6791BD605500001F96E44AB13331C9E; newhcproviderid=100021995974; memtypeid=0; areaname=%u4E94%u91D1; areaid=074; freeshop=1; maturity=2; Hm_lvt_1ad210f457c18335af4652c13d5766ce=1423966138,1425971502; Hm_lpvt_1ad210f457c18335af4652c13d5766ce=1425971502; BIGipServermyb2b_pool=3778193600.20480.0000; HC360_100021995974_isSitemove=1; WT_FPC=id=118.112.152.138-470302928.30423507:lv=1425971510159:ss=1425971502495; HC360.SecurityUser=20150310.151150-C2511822E5F00001696419AE6A5B5950-0-0-2; Hm_lvt_e1e386be074a459371b2832363c0d7e7=1423965214; Hm_lpvt_e1e386be074a459371b2832363c0d7e7=1425971512; hc5minbeat=1425971515856',
    'Host': 'www.hc360.com',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',
    'Referer': 'www.hc360.com',
}

url = "http://my.b2b.hc360.com/my/turbine/action/business.BusinAjaxAction"
attr_url = "http://my.b2b.hc360.com/my/turbine/template/corcenter%2Cbusiness%2Cstepsupplysecond.html"

hc_category = codecs.open("hc_category.json", "wb", encoding="utf-8")
hc_category_attr = codecs.open("hc_category_attr.json", "wb", encoding="utf-8")


def demo():
    begin = time.time()
    datas = get_all_id()
    for data in datas:
        sid = data["sid"]
        name = data["name"]
        line = json.dumps({"sid": sid, "name": name, "pid": "0", "cid": "0"}) + "\n"
        hc_category.write(line.decode("unicode_escape"))

        pool.spawn_n(get_category, sid)

    pool.waitall()

    print "Elapsed time: %s" % (time.time() - begin)

    hc_category.close()
    hc_category_attr.close()


def get_all_id():
    """获取所有分类的id"""
    params = {"path": "first"}
    result = requests.get(url, params=params, headers=headers)
    re_content = json.loads(result.content)
    re_data = re_content["data"]

    datas = []  # 包括分类id, 分类名称
    for data in re_data:
        datas.append({"name": data["name"], "sid": data["sid"]})

    return datas


def get_category(pid):
    data = {'path': 'next', 'sid': pid}
    result = requests.post(url, data=data, headers=headers)
    re_content = json.loads(result.content)
    re_data = re_content["data"]

    for data in re_data:
        sid = data["sid"]
        name = data["name"]
        cid = data["cid"]
        line = json.dumps({"sid": sid, "name": name, "pid": pid, "cid": cid}) + "\n"
        hc_category.write(line.decode("unicode_escape"))
        if data["hasNext"] == "1":  # 有下一级
            eventlet.sleep(0.5)
            get_category(sid)
        elif data["hasNext"] == "0":
            pool.spawn_n(get_category_attr, sid, cid)


def get_category_attr(sid, cid):
    data = {'supcatid': sid, 'catid': int(cid)}
    result = requests.post(attr_url, data=data, headers=headers)
    soup = BeautifulSoup(result.content)
    params = ""
    category_cg_items = soup.find(id="categoryCGItems")
    if category_cg_items:
        for li in category_cg_items.find_all("li"):
            params += li.get("data-paramname") if params == "" else "," + li.get("data-paramname")
    line = json.dumps({"sid": sid, "cid": cid, "attr": params}) + "\n"
    hc_category_attr.write(line.decode("unicode_escape"))


demo()
