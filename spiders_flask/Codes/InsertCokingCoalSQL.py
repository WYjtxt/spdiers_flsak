import os
import xlrd
import pymysql
from Configs import Config

# 创建sql连接并执行sql语句，最后关闭连接
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
    sql = "drop table if exists coking_coal_prices"
    connect(sql)

# 创建表
def create_table():
    sql = '''
    create table `coking_coal_prices` (
                `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                `mineCode` varchar(20)  NULL       COMMENT '煤矿编码',
                `contract_name` varchar(10)  NULL comment '合约名称',
                `open_price` double  NULL comment '今日开盘价',
                `close_price` double NULL comment '昨日收盘价',
                `settle_price` double NULL comment '昨日结算价',
                `trade_date` date NULL comment '交易日期'
                ) comment = '焦煤价格信息表';
                '''
    connect(sql)

# 插入数据
def insert2db():
    # 打开excel文件
    # filepath = './Data/coking_info_2023-5-8.xls'
    filepath = os.path.join(Config.DATA_DIR, 'cokingCoal.xls')
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
        contract_name = info[0]
        open_price = info[1]
        close_price = info[2]
        settle_price = info[3]
        trade_date = info[4]
        
        insert_sql = f'''
                    insert into coking_coal_prices(`mineCode`, `contract_name`, `open_price`, `close_price`, `settle_price`, `trade_date`)
                    values ('141029B0015000102916', '{contract_name}', {open_price}, {close_price}, {settle_price}, '{trade_date}')
                        '''
        connect(insert_sql)

# 调用函数
def insert_coking():
    # 删除原表，创建表，插入数据
    # delete_table()
    # create_table()
    insert2db()
    print('Insert Coking Coal Infos Completed!')

if __name__ == '__main__':
    insert_coking()
