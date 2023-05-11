from flask import Flask, jsonify  # 导入flask
from datetime import datetime   # 导入时间模块
from apscheduler.schedulers.background import BackgroundScheduler   # 定时任务

from Configs import get_dates    # 导入自定义模块
from Codes.InsertCoalSQL import insert_coal 
from Codes.InsertCokeSQL import insert_coke
from Codes.InsertCokingCoalSQL import insert_coking
from Codes.InsertSteamCoalSQL import insert_steam
from Codes.spider_coal import coal_spider
from Codes.spider_coke import coke_spider
from Codes.spider_coking import coking_spider
from Codes.spider_steam import steam_spider

spider_job = [coal_spider, coke_spider, coking_spider, steam_spider]    # 爬虫任务列表
insert_job = [insert_coal, insert_coke, insert_coking, insert_steam]    # 数据库插入任务列表

# 调度器在后台线程中运行，不会阻塞当前线程
scheduler = BackgroundScheduler()   # 实例化调度器

app = Flask(__name__)   # 实例化flask

# 启动函数，运行文件时自动启动
@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT', 'CATCH'])      # 路由
def begin():    
    print('启动成功！')
    return jsonify({'code': 200})

# 添加任务函数
def add_job(func, args= ()):    
    '''
    func：定时任务执行的函数名称。
    args：任务执行函数的位置参数，若无参数可不填
    id：任务id，唯一标识，修改，删除均以任务id作为标识
    trigger：触发器类型，参数可选：date、interval、cron, date执行一次、interval循环执行、cron定时执行
    replace_existing：将任务持久化至数据库中时，此参数必须添加，值为True。并且id值必须有。不然当程序重新启动时，任务会被重复添加。
    '''
    scheduler.add_job(func= func, args= args, id= f"{func}", trigger= "interval", days= 1, replace_existing= True)  # 添加任务

# 定时任务
def timedTask(execute_time, day_interval, month_interval, year_interval):
    now = datetime.now()
    work_dates, _ = get_dates.get_dates(day_interval= day_interval, month_interval= month_interval, year_interval= year_interval)   # 获取工作日列表
    try:
        if now.strftime('%Y-%m-%d') in work_dates:  # 判断今天是否为工作日
            hour = now.hour
            if hour == execute_time:
                # print(1)
                for spider in spider_job:
                    # print(2)
                    add_job(spider, args=(day_interval, month_interval, year_interval))
                for job in insert_job:
                    # print(3)
                    add_job(job)
    except Exception as e:  # 异常处理
        print(e)

# 主函数    
def run(execute_time= 20, day_interval= 0, month_interval= 0, year_interval= 0):
    '''
    :param execute_time: 定时任务执行时间，默认为20（20点）
    :param day_interval: 日间，默认为0
    :param month_interval: 月间，默认为0
    :param year_interval: 年间，默认为0
    :return: None
    '''
    timedTask(execute_time, day_interval, month_interval, year_interval)  # 定时任务
    scheduler.start()       # 启动任务列表
    app.debug = True        # 开启调试模式
    app.run(host='0.0.0.0', port=8000)      # 启动 flask

if __name__ == '__main__':
    # run(execute_time= 10)  # 需要更改爬取间隔时，写上全称，只写数字可能会被误认为其他参数。测试用
    run()