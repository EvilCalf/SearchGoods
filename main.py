import csv
import json
import os
import re
import time
import urllib.request

import requests
from lxml import etree

from config import cookie, dep, good

count = 1


def getHTMLText(url):
    me = {'cookie': cookie,
          'User-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=me, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html, page):
    view_price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
    if(len(view_price)==0):
        return
    detail_url = re.findall(r'\"detail_url\"\:\".*?\"', html)
    raw_tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
    item_loc = re.findall(r'\"item_loc\"\:\".*?\"', html)
    view_sales = re.findall(r'\"view_sales\"\:\".*?\"', html)
    comment_count = re.findall(r'\"comment_count\"\:\".*?\"', html)
    nick = re.findall(r'\"nick\"\:\".*?\"', html)
    picture = re.findall(r'\"pic_url\"\:\".*?\"', html)
    global count
    for i in range(len(view_price)):
        durl = json.loads('{'+detail_url[i]+'}')
        durl = ''.join(etree.HTML(durl['detail_url']).xpath('//text()'))
        price = eval(view_price[i].split(':')[1])
        rtlt = eval(raw_tlt[i].split(':')[1])
        loc = eval(item_loc[i].split(':')[1])
        sale = eval(view_sales[i].split(':')[1])
        ccout = eval(comment_count[i].split(':')[1])
        name = eval(nick[i].split(':')[1])
        pic = eval(picture[i].split(':')[1])
        pic=str(pic).replace("//","http://")
        urllib.request.urlretrieve(pic, good+'/%s.jpg' % count)
        ilt.append([count, price, rtlt, loc, sale, ccout, name, durl])
        count += 1


def main():
    goods = good
    depth = dep
    basic_url = 'https://s.taobao.com/search?q=' + goods
    uList = []
    header = ["序号", "价格", "商品名称", "地区", "销售数量", "评论数", "卖家名称", "详细链接"]

    if not os.path.exists(goods):
        os.mkdir(goods)

    for i in range(depth):
        try:
            url = basic_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(uList, html, i)
            print("第"+str(i+1)+"页爬取成功")
            time.sleep(0.5)
        except:
            continue
    filename = goods+".csv"

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in uList:
            writer.writerow(row)


if __name__ == '__main__':
    main()
