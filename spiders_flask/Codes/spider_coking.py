import csv
import os
import sys
import openpyxl
import requests
import urllib
from bs4 import BeautifulSoup
from Configs import Config, get_dates   # 获取工作日时间
sys.stdout.buffer.write(b'\xef\xbb\xbf')  # 将字节写入文本文件

# 1 爬取目标url
def select_url2xls(dates):
    url_list = []
    # 1.1 设置请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0"}
    # 1.2 爬取目标url
    for date in dates:
        try:
            url = f'https://www.quheqihuo.com/jiaomei/{date}/list_history_3503_1.html'
            url_text = requests.get(url, headers).content.decode('utf-8')   # 获取网页内容
            soup = BeautifulSoup(url_text, 'lxml')  # 解析网页
            border = soup.findAll("ul",{"class":"news_list_1"})  # 获取ul标签
            for i in range(len(border)):
                li = border[i].findAll("li")    # 获取li标签
                for l in li:
                    name = l.findAll("span",{"class" :"fr date"})   # 获取作者
                    aim_url = l.find("a")['href']    # 获取url
                    for n in name:
                        if "作者:--" in str(name):  # 如果作者为--，则爬取
                            url_list.append(aim_url)    # 将url添加到列表中
            # 1.3 将爬取的url写入excel
            with open(os.path.join(Config.DATA_DIR,"coking_net.xls"), 'w+', encoding='gb18030', newline= '') as f:
                for url in url_list:    
                    f.write(url + '\n') # 将url写入excel
        except Exception as e:
            print(e)
    return url_list   # 返回url列表

# 2. 解析网页
def parse_url(url_list):
    cok_infos = []
    single_info = []
    # 2.1 设置请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0"}
    for url in url_list:
        req = urllib.request.Request(url, headers=headers)  # 设置请求头
        webpage = urllib.request.urlopen(req)               # 打开网页
        html = webpage.read().decode('utf-8')               # 获取网页内容
        # 2.2 解析网页
        soup = BeautifulSoup(html.replace('&nbsp;',''), 'lxml')  # 解析网页
        # 2.3 获取标题
        tables = soup.find_all('table')  # 获取table标签
        for table in tables:
            tbodys = table.find_all('tbody')    # 获取tbody标签
            for tbody in tbodys:
                trs = tbody.find_all('tr')      # 获取tr标签
                for tr in trs:
                    td = tr.find_all('td')      # 获取td标签
                    for d in td:
                        single_info.append(d.string)    # 将信息添加到列表中
                cok_infos.append(single_info[:12])      
    return cok_infos

# 3. 保存数据
def save_data(info, dates, lendates):
    data_list = []
    try:
        for i in range(lendates):
            data_list.append(info[i][: 4] + [dates[i]])         # 将日期添加到列表中
            data_list.append(info[i][4: 8] + [dates[i]])
            data_list.append(info[i][8: ] + [dates[i]])
    except Exception as e:
        print(e, '，该日无可爬取信息！')
    with open(os.path.join(Config.DATA_DIR,'coking_info.csv'), 'w+', encoding= 'gb18030', newline= '') as f:
        for data in data_list:
            for i in data:
                f.write(i + ',')
            f.write('\n')
        f.seek(0)                   
        read = csv.reader(f)        # 读取csv文件
        wb = openpyxl.Workbook()    # 创建工作簿
        ws = wb.active              # 获取工作表
        for line in read:
            ws.append(line)         # 将csv文件内容写入excel
        wb.save(os.path.join(Config.DATA_DIR,'cokingCoal.xls'))  # 保存excel文件
    print('Spider Coking Coal Completed!')
    return data_list

# 调用函数
def coking_spider(day_interval= 0, month_interval=0, year_interval= 0):    # interval为爬取间隔（天）
    dates, lendates = get_dates.get_dates(day_interval, month_interval, year_interval)   #获取爬取日期
    url_list = select_url2xls(dates)     # 爬取目标url
    info = parse_url(url_list)          # 解析网页
    save_data(info, dates, lendates)    # 保存数据

if __name__ == "__main__":
    coking_spider() # 从4月1号到现在

