import os
import xlrd
import pymysql
from Configs import Config

# 创建mysql连接，执行SQL语句
def connect(sql):
    conn = pymysql.connect(host= Config.host,  # MYSQL服务器地址
                           user= Config.user,  # 用户名
                           password= Config.password,  # 密码
                           port= Config.port,  # 端口
                           db= Config.db,  # 数据库连接名
                           charset='utf8')  # 编码方式
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

# 删除表
def delete_table():
    sql = "drop table if exists `steam_coal_prices`"
    connect(sql)

# 创建表
def create_table():
    sql = '''
    create table `steam_coal_prices` (                                  
                `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                `mineCode` varchar(20)  NULL comment '煤矿编码',
                `contract_name` varchar(10) NULL comment '合约名称',
                `latest_price` double NULL comment '今日最新价',
                `close_price` double NULL comment '昨日收盘价',
                `trade_date` date NULL comment '交易日期'
                ) comment = '动力煤价格信息表';
                '''
    connect(sql)

# 插入数据
def insert2db():
    # 打开excel文件
    # filepath = './Data/steamCoal_2023-5-8.xls'
    filepath = os.path.join(Config.DATA_DIR, 'steamCoal.xls')
    wkb = xlrd.open_workbook(filepath)
    # 获取sheet
    sheet = wkb.sheet_by_index(0)  # 获取第一个sheet表
    # 获取总行数
    rows_number = sheet.nrows
    # 遍历sheet表中所有行的数据，并保存至一个空列表中
    cap = []
    for i in range(rows_number):
        x = sheet.row_values(i)  # 获取第i行的值
        cap.append(x)
    # print(cap)

    # 将读取到的数据批量插入数据库
    for info in cap:
        contract_name = info[0]
        latest_price = info[1]
        close_price = info[2]
        trade_date = info[3]

        insert_sql = f'''
                    insert into `steam_coal_prices`(`mineCode`, `contract_name`, `latest_price`, `close_price`, `trade_date`)
                    values ('141029B0015000102916', '{contract_name}', {latest_price}, {close_price}, '{trade_date}')
                        '''
        connect(insert_sql)

# 调用函数
def insert_steam():
    # delete_table()
    # create_table()
    insert2db()
    print('Insert Steam Coal Infos Completed！')

if __name__ == '__main__':
    insert_steam()
