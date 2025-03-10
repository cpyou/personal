import pandas as pd
from datetime import datetime, timedelta

# 定义2024年的开始和结束日期
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# 创建空列表存储日期和周数
dates = []
weeks = []

# 循环生成每一天的日期和对应的周数
current_date = start_date
while current_date <= end_date:
    # 日期格式化为YYYYMMDD
    dates.append(current_date.strftime("%Y%m%d"))

    # 计算自然周（从1月1日开始的周数，每周7天）
    day_of_year = current_date.timetuple().tm_yday  # 获取一年中的第几天
    week_number = (day_of_year - 1) // 7 + 1  # 计算周数（从1开始）
    weeks.append(f"{current_date.strftime('%y')}年WK{week_number}")  # 格式化为24年WK1

    current_date += timedelta(days=1)  # 增加一天

# 创建DataFrame并保存为Excel
pd.DataFrame({"Date": dates, "Week": weeks}).to_excel("2024_dates_and_weeks.xlsx", index=False)

print("Excel文件已生成：2024_dates_and_weeks.xlsx")
