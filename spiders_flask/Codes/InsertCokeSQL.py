import os
import xlrd
import pymysql
from Configs import Config

# 创建链接，执行SQL语句
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
    sql = "drop table if exists `coke_prices`"
    connect(sql)

# 创建表
def create_table():
    sql = '''
    create table `coke_prices` (
                `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                `mineCode` varchar(20) NULL COMMENT '煤矿编码',
                `futures_name` varchar(20) NULL COMMENT '期货名称',
                `open_price` double NULL COMMENT '今日开盘价',
                `close_price` double NULL COMMENT '昨日收盘价',
                `trade_date` date NULL COMMENT '交易日期'
                ) COMMENT = '焦炭价格信息表'; 
                '''
    connect(sql)

# 插入数据
def insert2db():

    # 打开excel文件
    # filepath = './Data/coke_2023-5-8.xls'
    filepath = os.path.join(Config.DATA_DIR, 'coke.xls')
    wkb = xlrd.open_workbook(filepath)
    # 获取sheet
    sheet = wkb.sheet_by_index(0)   # 获取第一个sheet表
    # 获取总行数
    rows_number = sheet.nrows
    # 遍历sheet表中所有行的数据，并保存至一个空列表中
    cap = []
    for i in range(rows_number):
        x = sheet.row_values(i) # 获取第i行的值
        cap.append(x)
    # print(cap)

    # 将读取到的数据批量插入数据库
    for info in cap:
        futures_name = info[0]
        open_price = info[1]
        close_price = info[2]
        trade_date = info[3]

        insert_sql = f'''
                    insert into `coke_prices`(mineCode, futures_name, open_price, close_price, trade_date)
                    values ('141029B0015000102916', '{futures_name}', {open_price}, {close_price}, '{trade_date}')
                        '''
        connect(insert_sql)

# 调用函数
def insert_coke():
    # 删除原表，创建表，插入数据
    # delete_table()
    # create_table()
    insert2db()
    print('Insert Coke Infos Completed！')

if __name__ == '__main__':
    insert_coke()
