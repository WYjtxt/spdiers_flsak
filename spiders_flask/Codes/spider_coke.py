import os
import csv
import sys
import openpyxl
import requests
import urllib
from lxml import etree
from bs4 import BeautifulSoup
from Configs import Config, get_dates
sys.stdout.buffer.write(b'\xef\xbb\xbf')  # 将字节写入文本文件

# 1.爬取网页
def get_all_html(lendates):
    # 获取网址，打开开发者模式定位目标信息的位置，记录位置关键词，方便解析
    all_urls = 'https://futures.cngold.org/jiaotan/list_2533_all.html'
    # 获取请求头. Network下进行翻页操作，点击链接，右方出现Headers可查看具体信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
    url_list = []
    all_html = requests.get(url= all_urls, headers= headers, timeout= 30).content.decode('utf-8')   # 爬取前了解并遵守robots协议，不要频繁访问
    lx_all_html = etree.HTML(all_html)
    urls = lx_all_html.xpath('//div[@class="history_news_content"]/ul/li/a/@href')[: lendates]     # 爬取4月数据时,lendates+2
    for i in urls:
        one_html = requests.get(i).content.decode('utf-8')
        lx_one_html = etree.HTML(one_html)
        last_url = lx_one_html.xpath('//div[@class="border_top"]/ul/li/a/@href') # xpath返回ul里的所有url列表
        url_list.append(last_url)
    # print(url_list)
    return url_list

# 存储网页信息
def generate_coke_net(len_dates):
    urllist = []
    url_final_list = []
    url_list = get_all_html(len_dates)
    for i in url_list:
        for j in i:
            if ('2023' in j):   # 滤除干扰项,目标网页含有日期
                urllist.append(j)
    for url in urllist:
        url = ''.join(url)  # 去掉链接的单引号
        url_final_list.append(url)
    with open(os.path.join(Config.DATA_DIR, 'coke_net.csv'), 'w+', newline='') as f1:  # 将爬取到的最终网页保存到coke_net文件中
        for url in url_final_list:
            f1.write(url + '\n')

# 2.解析网页
def fill_into_list(soup):
    all_info = []
    table = soup.find_all('table')
    for ul in table:
        single_info = []
        lspan = ul.find_all('tbody')
        for span in lspan:
            la = span.find_all('tr')
            for a in la:
                lb = a.find_all('td')
                for b in lb:
                    single_info.append(b.string)
            all_info.append(single_info)
    return all_info[0]

# 3.保存数据
def save2slx():
    date_list = []  # 存储网页发布的日期
    coke_list = []  # 存储焦炭价格信息
    with open(os.path.join(Config.DATA_DIR,'coke_net.csv'), 'r') as f1:   # 保存网址信息
        urls = f1.readlines()
        for url in urls:
            # 获取网页发布日期
            date = url[29:39]
            date_list.append(date)
            # 获取网页文本
            req = urllib.request.Request(url)  # 发起请求
            webpage = urllib.request.urlopen(req)  # 打开网页
            html = webpage.read().decode()  # 读取网页所有信息
            # 解析网页文本信息
            soup = BeautifulSoup(html.replace('&nbsp;', ''), "lxml")
            info_list = fill_into_list(soup)
            coke_list.append(info_list)
    coke_data = []
    lendata = len(date_list)
    for i in range(lendata):
        coke_data.append(coke_list[i][0:3] + [date_list[i]])    # 期货类型 + 开盘价 + 昨收价 + 日期   0 - 3
        coke_data.append(coke_list[i][3:6] + [date_list[i]])
        coke_data.append(coke_list[i][6:] +[ date_list[i]])
    coked = coke_data.copy()
    coked.reverse()
    with open(os.path.join(Config.DATA_DIR,'coke_info.csv'), 'w+', newline='',encoding= 'gb18030') as f2:     # 保存焦炭数据
        for coke in coked:
            for i in coke:
                f2.write(i + ',')
            f2.write('\n')
        f2.seek(0)
        with open(os.path.join(Config.DATA_DIR, 'coke_final_info.csv'), 'w+', newline='', encoding= 'gb18030') as f3:    # 去掉每行末尾的逗号
            for line in f2.readlines():
                line = line[:-2]
                f3.write(line)
                f3.write('\n')
    # 将csv转化为xls文件，方便入库
    with open(os.path.join(Config.DATA_DIR, 'coke_final_info.csv'), 'r', encoding='gb18030') as cf:
        read = csv.reader(cf)
        wb = openpyxl.Workbook()
        ws = wb.active
        for line in read:
            ws.append(line)
        wb.save(os.path.join(Config.DATA_DIR,'coke.xls'))
    print("Spider Coke Completed!")

# 调用函数
def coke_spider(day_interval= 0, month_interval= 0, year_interval= 0):
    dates, len_dates = get_dates.get_dates(day_interval, month_interval, year_interval)   # 调用函数输出日期
    generate_coke_net(len_dates)    # 生成网页信息    爬取4-3到5-10，在此处+2
    save2slx()  # 调用解析网页函数并将解析得到的数据保存到excel中

if __name__ == '__main__':
    coke_spider()