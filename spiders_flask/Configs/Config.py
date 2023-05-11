# 数据库配置信息

# 本地数据库
host= '192.168.14.94'       # MYSQL服务器地址
user= 'root'              # 用户名
password= '123456'       # 密码
port= 3306                # 端口
db= 'spiders'         # 数据库名

# 对接数据库,连不上
# host= '10.10.1.21'       # MYSQL服务器地址
# user= 'root'              # 用户名
# password= 'ygsj!2q'       # 密码
# port= 3308                 # 端口
# db= 'sxygsj-zhgk'         # 数据库名

# 路径统一配置
import os

# 项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, 'Logs')

# 配置文件路径
CONF_DIR = os.path.join(BASE_DIR, 'Config')

# 存放数据路径
DATA_DIR = os.path.join(BASE_DIR, 'Data')

# 代码路径
CODE_DIR = os.path.join(BASE_DIR, 'Codes')

if __name__ == '__main__':
    print(BASE_DIR)
    print(CODE_DIR)
