import os
import csv
import openpyxl
import pandas as pd
import requests
from lxml import etree
from bs4 import BeautifulSoup
from Configs import Config, get_dates

# 自定义类，用于煤炭信息爬取
class Spider_info:
    # 1. 初始化，传入爬取数据的天数
    def __init__(self, day_interval, month_interval= 0, year_interval= 0):
        self.dates, self.len_dates = get_dates.get_dates(day_interval, month_interval, year_interval)
        self.url = 'https://www.cngold.org/meitan/list_112_all.html'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
        self.timeout = 30

    # 1. 获取url信息
    def get_url(self):
        url_list = []
        final_urls = []
        all_html = requests.get(url= self.url, headers= self.headers, timeout= self.timeout).content.decode('utf8')  # 获取网页信息
        html = etree.HTML(all_html) # 解析网页
        urls = html.xpath('//div[@class="history_news_content"]/ul/li/a/@href')[: self.len_dates] # 获取所有url
        for url in urls:
            one_html = requests.get(url= url, headers= self.headers, timeout= self.timeout).content.decode('utf8') # 获取单个url信息
            lx_one_html = etree.HTML(one_html) # 解析单个url信息
            last_url = lx_one_html.xpath('//div[@class="border_top"]/ul/li/a/@href') # 获取最后的url列表
            url_list.append(last_url)   # 添加到列表中
        # print(url_list)
        url_list = [i[0] for i in url_list] # 将列表中的列表转换为列表
        for url in url_list:
            url = ''.join(url)  # 将列表转换为字符串
            final_urls.append(url)  # 添加到列表中
        final_urls.reverse()    # 列表反转，日期从远到近
        return final_urls

    # 2. 解析网页
    # 2.1 获取网页信息
    def fill_content(self, soup):
        all_info = []
        tables = soup.find_all('table')         # 获取所有的table标签
        for table in tables:
            single_info = []
            tbodys = table.find_all('tbody')    # 获取所有的tbody标签
            for tbody in tbodys:
                trs = tbody.find_all('tr')      # 获取所有的tr标签
                for tr in trs:
                    tds = tr.find_all('td')     # 获取所有的td标签
                    for td in tds:
                        single_info.append(td.string)   # 获取td标签中的内容
                all_info.append(single_info)    # 将单个信息添加到列表中
        all_info = all_info[0]
        return all_info

    # 2.2 解析网页
    def parse_url(self, urls):
        coal_info = []
        for url in urls:
            html = requests.get(url= url, headers= self.headers, timeout= self.timeout).content.decode('utf-8') # 获取网页信息
            # 解析网页
            soup = BeautifulSoup(html.replace('&nbsp;', ''), 'lxml')    # 解析网页
            all_info = self.fill_content(soup)  # 获取网页信息
            coal_info.append(all_info)  # 将网页信息添加到列表中
        return coal_info

    # 3. 保存信息
    # 3.1 列表切片，变形
    def asize(self, arr, size):
        s = []
        for i in range(0, int(len(arr)), size):     # 从start=0开始，到stop=int(len(arr))结束，步长为step=size
            c = arr[i: i + size]                # 切片
            s.append(c)                        # 添加到列表中
        return s    # 返回切片后的列表

    # 3.2 保存信息
    def save_raw2csv(self, coal_info):
        try:
            last = []
            with open(os.path.join(Config.DATA_DIR, 'Coal_info.csv'), 'w+', newline= '') as f:
                for i in coal_info:
                    for j in i:
                        last.append(j)
                last = self.asize(last, 5)  # 切片
                writer = csv.writer(f)  # 写入csv文件
                for row in last:
                    writer.writerow(row)
        except Exception as e1:
            print('e1: ',e1)

    # 读取列
    def open_file(self, file_name, encoding= 'utf8'):
        try:
            with open(os.path.join(Config.DATA_DIR, f'{file_name}.csv'), 'rt', encoding= encoding) as csvfile:
                reader = csv.reader(csvfile)
                column = [row[0] for row in reader]
                return len(column), column
        except Exception as e2:
            print('e2: ', e2)
            return None, None

    # 扩充省份，并将其与爬取到的数据进行拼接
    def fill_coal(self):
        urls = self.get_url()   # 获取urls列表
        coal_info = self.parse_url(urls)    # 解析网页
        self.save_raw2csv(coal_info)    # 将原始数据保存到csv文件中
        lenc1, c1  = self.open_file('pro_info', encoding= 'utf-8')
        lenc2, c2 = self.open_file('Coal_info')
        n = lenc2 // lenc1
        pro = c1
        pro_info = []
        for i in range(n):
            pro_info.append(pro)
        pro_info = [x for item in pro_info for x in item]  # 将嵌套列表的内层中括号去掉
        with open(os.path.join(Config.DATA_DIR, 'pro_all_info.csv'), 'w+', encoding= 'gb18030', newline= '') as f:
            for i in range(len(pro_info)):
                f.write(pro_info[i] + '\n')
        df1 = pd.read_csv(os.path.join(Config.DATA_DIR, 'pro_all_info.csv'), encoding= 'gb18030', header= None)
        df2 = pd.read_csv(os.path.join(Config.DATA_DIR, 'Coal_info.csv'), encoding= 'utf8', header= None)
        file = [df1, df2]
        df = pd.concat(file, axis= 1)
        df.columns = range(6)
        # df.columns = ['provinces', 'city', 'coal_types', 'coal_names', 'coal_prices', 'trade_time'] # 重置列索引
        df.to_csv(os.path.join(Config.DATA_DIR, 'coal_final.csv'), header= None,sep= ',')
        with open(os.path.join(Config.DATA_DIR, 'coal_final.csv'), 'r', encoding= 'utf-8') as f:
            read = csv.reader(f)
            wb = openpyxl.Workbook()
            ws = wb.active
            for line in read:
                ws.append(line)
            wb.save(os.path.join(Config.DATA_DIR, 'coal.xls'))
        return df

    # 类内调用程序
    def run_coal(self):
        self.fill_coal()
        print('Spider Coal Completed!')

# 实例化类调用程序，方便进行定时任务
def coal_spider(day_interval= 0, month_interval= 0, year_interval= 0):
    spider = Spider_info(day_interval,month_interval, year_interval)
    spider.run_coal()

if __name__ == '__main__':
    # coal_spider(6, 1)   # 5-10
    coal_spider()