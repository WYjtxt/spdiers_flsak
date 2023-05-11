import chinese_calendar
from datetime import datetime, timedelta

# 获取工作日
def get_workdays_nowadays(year, month, day=1):
    try:
        work_days = chinese_calendar.get_workdays(datetime(year= year, month= month, day= day), datetime.now())
        date_list = []
        for work_day in work_days:
            date_list.append(work_day.strftime("%Y-%m-%d"))
        return date_list, len(date_list)
    except Exception as e:
        print("输入错误")

# 上述函数功能扩展，随机输入日月年，得到当时到现在的工作日列表及长度
def get_dates(day_interval= 0, month_interval= 0, year_interval= 0):
    # 0 因为该网站基本上在工作日发布煤炭相关信息的咨询，需要获取工作日时间并计算爬取的总数
    if day_interval in range(datetime.now().day):
        year, month, day = datetime.now().year - year_interval, datetime.now().month - month_interval, datetime.now().day - day_interval  # 获取当前年月日
        dates, len_dates = get_workdays_nowadays(year, month, day)  # 获取工作日时间
    else:
        raise ValueError('Value of interval you entered is not in the normal range！')
    return dates, len_dates

if __name__ == '__main__':
    dates, len_dates = get_dates(1)
    print(dates, len_dates)
    now = datetime.now() - timedelta(days= 2)
    now_date = now.strftime('%Y-%m-%d')
    print(now_date)
    if now_date in dates:
        print(111)
    else:
        print(222)