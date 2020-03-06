# -*- coding: UTF-8 -*-
# =================================================
#      language       ： Python3.7
#      IDLE           :  pycharm
#      Date           :  17/04/2019
# =================================================
import datetime
import os
import re
import requests
import xlsxwriter
from urllib.parse import quote


class Weather2345(object):
    def __init__(self, city=None):
        self.city = city
        self.bm_url = 'https://tianqi.2345.com/t/searchCity.php?pType=local&q='
        self.ua = 'Mozilla/5.0 '
        self.ref = 'https://tianqi.2345.com/'
        self.headers = {'User-Agent': self.ua, 'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Referer': self.ref}
        self.query_headers = {'User-Agent': self.ua, 'Referer': self.ref,
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    def get_city_code(self):
        try:
            r = requests.get(url=self.bm_url + quote(self.city), headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            data = r.json()
            if data['res'][0]['href']:
                return data['res'][0]['href']
            else:
                print('没有' + self.city + '的天气信息')
        except requests.ConnectionError as e:
            print('Erro')

    def get_html(self):
        url = 'https://tianqi.2345.com' + self.get_city_code()
        try:
            r = requests.get(url=url, headers=self.query_headers)
            r.raise_for_status()
            r.encoding = 'GBK'
            return r.text
        except requests.ConnectionError as e:
            print('Error')

    def parsed_data(self):
        text = self.get_html()
        r = re.compile(r'<p>.*?<strong>([^<]+)\(<font.*?>([^<]+)</font>\).*?<b>([^<]+)</b>.*?<i><font class="blue">' \
                       '([^<]+)</font>～<font class="red">([^<]+)</font><br.*?((?<=>)[^<]+)</i>', re.M | re.S)
        result = re.findall(r, text)
        fbsj = 'From:2345天气预报'
        print('  -----' + self.city + '天气预报' + '(未来' + str(len(result)) + '天）' + fbsj + '-----')
        print('-' * 60)
        format_result = []
        for p in result:
            p = [item.strip() for item in p]
            format_result.append(p)
            p0, p1, p2, p3, p4, p5 = p
            print("  {0:^6}\t {1:^2}\t{2:{6}<6}\t{3:{6}<4}\t{4:{6}^3}\t{5:{6}<6}".format(p0, p1, p2, p3, p4,
                                                                                         p5.replace(' ', ''),
                                                                                         chr(12288)))
        print('-' * 60)
        return format_result


header_format = {
    'bold':  True,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#F4B084',  # 单元格背景颜色
    'text_wrap': True,  # 是否自动换行
}

default_format = {
    'bold':  False,  # 一般字体
    'border': 1,  # 单元格边框宽度
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#F4B084',  # 单元格背景颜色
    'text_wrap': True,  # 是否自动换行
}

city_format = {
    'bold':  False,  # 一般字体
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#F4B084',  # 单元格背景颜色
    'text_wrap': True,  # 是否自动换行
}


def write_data_2_xlsx(filename=None, cities_weather_data=None):
    filename = filename or 'test.xlsx'
    cities_weather_data = cities_weather_data or []
    wbk = xlsxwriter.Workbook(filename=filename)
    header_style = wbk.add_format(header_format)
    default_style = wbk.add_format(default_format)
    city_style = wbk.add_format(city_format)
    sheet = wbk.add_worksheet('sheet1')
    columns = [f'{item[0]} {item[1]}' for item in cities_weather_data[0][1]]
    sheet.set_column(1, len(columns), 13)

    sheet.write_row(0, 1, columns, header_style)
    row = 1
    height = 3
    for city_weather in cities_weather_data:
        weather = city_weather[1]
        col = 0
        last_row = row + height - 1
        sheet.merge_range(first_row=row, last_row=last_row,
                          first_col=col, last_col=col,
                          data=city_weather[0], cell_format=city_style)
        for item in weather:
            d = [item[2], f'{item[3]}~{item[4]}', item[5]]
            col += 1
            sheet.write_column(row, col, d, default_style)
        row += height
    wbk.close()


def generate_cities_weather_forecast_xlsx():
    cities = ['上海', '南京', '杭州', '宁波', '金华', '青岛', '徐州', '济南', '合肥', '苏州', '无锡', '镇江', '马鞍山', '南通', '绍兴', '芜湖']
    data = []
    for city in cities:
        result = Weather2345(city).parsed_data()
        data.append((city, result))

    home_path = os.path.expanduser('~')
    xlsx_name = f'{home_path}/Desktop/天气预报-{str(datetime.date.today())}.xlsx'
    write_data_2_xlsx(filename=xlsx_name, cities_weather_data=data)
    return xlsx_name


if __name__ == '__main__':
    generate_cities_weather_forecast_xlsx()
