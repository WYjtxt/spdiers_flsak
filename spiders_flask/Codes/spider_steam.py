import os           # 导入os库
import csv          # 导入csv库
import sys          # 导入sys库
import urllib       # 导入urllib库
import openpyxl     # 导入openpyxl库
import requests     # 导入requests库
from lxml import etree  # 导入xpath库
from bs4 import BeautifulSoup   # 导入BeautifulSoup库
from Configs import Config, get_dates    # 导入获取当前年月的工作日列表的函数
sys.stdout.buffer.write(b'\xef\xbb\xbf')    # 解决csv文件中文乱码问题

# 定义类，用于动力煤价格信息的爬取
class SteamCoalSpider:
    # 初始化
    def __init__(self, date_list, date_num):
        self.date = date_list   # 日期列表
        self.num = date_num    # 日期天数

    # 1. 爬取网页
    def select_url2xls(self):   # 选择url并写入xls文件
        url_list = []
        base_url = 'https://www.quheqihuo.com/donglimei/list_3497_all.html'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0"}
        try:
            source_webpage = requests.get(base_url, headers=headers, timeout= 30).content.decode('utf-8') # 获取网页源码
            lx_webpage = etree.HTML(source_webpage) # 转换为xpath可解析的格式
            urls = lx_webpage.xpath('//div[@class="history_news_content"]/ul/li/a/@href')[: self.num]   # 获取截至当前时间内，本月的所有url
            for url in urls:
                req = requests.get(url, headers=headers).content.decode('utf-8')    # 获取网页源码
                lx_final_url = etree.HTML(req)  # 转换为xpath可解析的格式
                final_url = lx_final_url.xpath('//div[@class="border_top"]/ul/li/a/@href')  # 获取最终的url列表
                url_list.append(final_url)  # 将每一天的url添加到列表中
            urls = sum(url_list, [])    # 将二维列表转换为一维列表
            return urls
        except Exception as e:
            print('Error:', e)
            return None

    # 2. 解析网页，获取数据
    @staticmethod   # 静态方法
    def parser_webpage(urls):       # 解析网页
        all_info = []
        single_info = []
        for url in urls:    # 遍历url列表
            try:
                html = urllib.request.urlopen(url).read().decode('utf-8')  # 获取网页文本
                soup = BeautifulSoup(html, 'lxml')  # 解析网页
                tables = soup.find_all('table')     # 获取网页中的所有表格
                for table in tables:
                    trs = table.find_all('tr')      # 获取表格中的所有行    
                    for tr in trs:  
                        tds = tr.find_all('td')     # 获取行中的所有列  
                        for td in tds:
                            single_info.append(td.string)   # 将每一列的数据添加到列表中
                    all_info.append(single_info[: 9])       # 将每一行的数据添加到列表中
            except Exception as e:  # 捕获异常
                print('Error:', e)  # 打印异常信息
        return all_info    # 返回列表

    # 3. 将数据写入xls文件
    def save_data(self, infos): 
        data_list = []  # 创建一个空列表，用于存储数据
        length = len(self.date)    # 获取日期列表的长度
        for i in range(length):
            data_list.append(infos[i][: 3] + [self.date[i]])    # 将日期添加到列表中
            data_list.append(infos[i][3: 6] + [self.date[i]])
            data_list.append(infos[i][6: ] + [self.date[i]])
        with open(os.path.join(Config.DATA_DIR, 'steamCoal.csv'), 'w+', encoding= 'gb18030', newline= '') as f: # w+,可读写; a+,追加
            for data in data_list:  # 将数据写入csv文件
                for i in data:    # 将每一行的数据写入csv文件
                    f.write(i + ',')    # 写操作
                f.write('\n')
            f.seek(0)       # 将文件指针移动到文件开头
            read = csv.reader(f)    # 读取csv文件
            wb = openpyxl.Workbook()   # 创建xls文件
            ws = wb.active      # 获取当前活跃的工作表
            for line in read:   # 读操作
                ws.append(line)     # 将csv文件中的数据写入xls文件
            wb.save(os.path.join(Config.DATA_DIR, 'steamCoal.xls'))    # 保存xls文件
            print('Spider Steam Coal Completed!')
        return data_list

# 调用函数,day_interval为日间间隔，month_interval为月间间隔，默认为零
def steam_spider(day_interval= 0, month_interval= 0, year_interval= 0):
    date_list, date_Num = get_dates.get_dates(day_interval,  month_interval, year_interval)    # 获取日期
    scp = SteamCoalSpider(date_list, date_Num)  # 实例化类
    urls = scp.select_url2xls()    # 获取网页url
    infos = scp.parser_webpage(urls)    # 获取网页数据
    scp.save_data(infos)    # 将数据写入xls文件

if __name__ == '__main__':
    # steam_spider(9, 1)  # 调用主函数,4-1-现在
    steam_spider()