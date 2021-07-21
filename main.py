import requests
import re
import csv
import time
from lxml import etree
import json
from config import cookie, good, dep

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
    try:
        view_price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        if(len(view_price)==0):
            return
        detail_url = re.findall(r'\"detail_url\"\:\".*?\"', html)
        raw_tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        item_loc = re.findall(r'\"item_loc\"\:\".*?\"', html)
        view_sales = re.findall(r'\"view_sales\"\:\".*?\"', html)
        comment_count = re.findall(r'\"comment_count\"\:\".*?\"', html)
        nick = re.findall(r'\"nick\"\:\".*?\"', html)

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
            ilt.append([count, price, rtlt, loc, sale, ccout, name, durl])
            count += 1
    except:
        print("")


def main():
    goods = good
    depth = dep
    basic_url = 'https://s.taobao.com/search?q=' + goods
    uList = []
    header = ["序号", "价格", "商品名称", "地区", "销售数量", "评论数", "卖家名称", "详细链接"]

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
