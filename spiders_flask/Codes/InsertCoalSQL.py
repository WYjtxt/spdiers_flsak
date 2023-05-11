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
    delete_sql = 'drop table if exists `coal_prices`'
    connect(delete_sql)

# 创建表
def create_table():
    create_sql = '''CREATE TABLE `coal_prices` (
                            `id`  int NOT NULL AUTO_INCREMENT,
                            `mineCode` varchar (20) NULL comment '煤矿编码',
                            `province` varchar (10) NULL comment '产地省份',
                            `city_name`  varchar(10)  NULL comment '煤炭产地',
                            `coal_types`  varchar(10)  NULL    comment '煤炭品种',
                            `coal_names`  varchar(10)  NULL      comment '煤炭品名',
                            `coal_price`  double  NULL      comment '煤炭价格',
                            `trade_time`  date  NULL   comment '交易时间',
                            PRIMARY KEY (`id`)
                            ) comment = '各地煤炭价格信息表';
                            '''
    connect(create_sql)

# 插入数据
def insert2db():
    # 打开excel文件
    # filepath = './Data/coal_info_2023-5-8.xls'
    filepath = os.path.join(Config.DATA_DIR, 'coal.xls')
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
        province = info[1]
        city_name = info[2]
        coal_types = info[3]
        coal_names = info[4]
        coal_price = info[5]
        trade_time = info[6]

        insert_sql = f'''
                    insert into coal_prices(`mineCode`, `province`, `city_name`, `coal_types`, `coal_names`, `coal_price`, `trade_time`)
                    values ('141029B0015000102916', '{province}', '{city_name}', '{coal_types}', '{coal_names}', {coal_price}, '{trade_time}')
                        '''
        connect(insert_sql)

# 调用函数
def insert_coal():
    # print(os.getcwd())
    # delete_table()
    # create_table()
    insert2db()
    print('Insert Coal Infos Completed!')

if __name__ == '__main__':
    insert_coal()
