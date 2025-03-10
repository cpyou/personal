import datetime
import pandas as pd


def get_week_range(year, week):
    """
    获取指定年份和周数的日期段（周一到周日）。
    """
    # 获取该周的第一天（周一）
    start_of_week = datetime.date.fromisocalendar(year, week, 1)
    # 获取该周的最后一天（周日）
    end_of_week = start_of_week + datetime.timedelta(days=6)
    return start_of_week, end_of_week


def generate_year_week_table(year):
    """
    生成指定年份的每周日期段表格。
    """
    # 获取该年的总周数
    result = []
    last_day_of_year = datetime.date(year, 12, 31)
    num_weeks = last_day_of_year.isocalendar()[1]
    if num_weeks == 1:
        num_weeks = datetime.date(year, 12, 31 - last_day_of_year.isocalendar()[2]).isocalendar()[1]

    # 打印表格标题
    print(f"+--------+----------------+----------------+")
    print(f"| 第几周 | 开始日期 (周一) | 结束日期 (周日) |")
    print(f"+--------+----------------+----------------+")

    # 遍历每一周
    for week in range(1, num_weeks + 1):
        start_of_week, end_of_week = get_week_range(year, week)
        start_month = start_of_week.strftime('%m')
        end_month = end_of_week.strftime('%m')
        if start_month == end_month:
            print(f"| {year}年{start_month}月wk{week:} | {start_of_week.strftime('%m.%d')}-{end_of_week.strftime('%m.%d')}    |")
            result.append((f'{year}年{start_month}月wk{week:}', f"{start_of_week.strftime('%m.%d')}-{end_of_week.strftime('%m.%d')}"))
        else:
            print(f"| {year}年{start_month}月-{end_month}月wk{week} | {start_of_week.strftime('%m.%d')}-{end_of_week.strftime('%m.%d')}    |")
            result.append((f'{year}年{start_month}月-{end_month}月wk{week}',
                           f'{start_of_week.strftime("%m.%d")}-{end_of_week.strftime("%m.%d")}'))

    print(f"+--------+----------------+----------------+")
    return result


# 示例：生成 2023 年的每周日期段表格
year = 2024
res = generate_year_week_table(year)
df = pd.DataFrame(res)
df.to_excel(f"{year}年每周日期段表格.xlsx", index=False, header=False)
