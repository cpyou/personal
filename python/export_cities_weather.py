# -*- coding: UTF-8 -*-
# =================================================
#      language       ： Python3.7
#      IDLE           :  pycharm
#      Date           :  17/04/2019
# =================================================
import datetime
import os
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from urllib.parse import quote
from io import BytesIO
from datetime import date

import requests
import xlsxwriter


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
            # r.encoding = 'GBK'
            return r.text
        except requests.ConnectionError as e:
            print('Error')

    def parsed_data(self):
        text = self.get_html()
        # r = re.compile(r'<p>.*?<strong>([^<]+)\(<font.*?>([^<]+)</font>\).*?<b>([^<]+)</b>.*?<i><font class="blue">' \
        #                '([^<]+)</font>～<font class="red">([^<]+)</font><br.*?((?<=>)[^<]+)</i>', re.M | re.S)
        re_pattern = r'<em>([^<]+)<em.*?<em>([^<]+)</em>.*?<font>([^<]+)</font>.*?<b>([^<]+)</b>.*?<b>([^<]+)</b>'
        r = re.compile(re_pattern, re.M | re.S)
        wea_result = re.findall(r, text)
        re_data_pattern = r"hoverAnimation: false.*?data:\s+(.*?),\n.*?type: 'line'"
        re_data_compile = re.compile(re_data_pattern, re.M | re.S)
        re_data_result = re.findall(re_data_compile, text)
        temp_data = list(zip(*[json.loads(item) for item in re_data_result]))

        fbsj = 'From:2345天气预报'
        print('  -----' + self.city + '天气预报' + '(未来' + str(len(wea_result)) + '天）' + fbsj + '-----')
        print('-' * 60)
        format_result = []
        for p in wea_result:
            p = [item.strip() for item in p]
            format_result.append(p)

        print('-' * 60)
        result = []
        for i in range(len(format_result)):
            result.append(format_result[i] + list(temp_data[i]))
        for item in result:
            p0, p1, p2, p3, p4, p5, p6 = item
            print("  {0:^6}\t {1:^7}\t{2:{7}<6}\t{3:{7}<4}\t{4:{7}^3}\t{5}\t{6}".format(p0, p1, p2, p3, p4, p5, p6,
                                                                                         chr(12288)))
        return result


header_format = {
    'bold':  True,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#cccccc',  # 单元格浅灰色
    'text_wrap': True,  # 是否自动换行
}

default_format0 = {
    'bold':  False,  # 一般字体
    'border': 1,  # 单元格边框宽度
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#FFFFFF',  # 单元格白色
    'text_wrap': True,  # 是否自动换行
}

default_format1 = {
    'bold':  False,  # 一般字体
    'border': 1,  # 单元格边框宽度
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#DCDCDC',  # 单元格钢蓝浅色
    'text_wrap': True,  # 是否自动换行
}

city_format = {
    'bold':  False,  # 一般字体
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#cccccc',  # 单元格浅灰色
    'text_wrap': True,  # 是否自动换行
}


def write_data_2_workbook(wbk, cities_weather_data=None):
    cities_weather_data = cities_weather_data or []
    header_style = wbk.add_format(header_format)
    default_style0 = wbk.add_format(default_format0)
    default_style1 = wbk.add_format(default_format1)
    city_style = wbk.add_format(city_format)
    sheet = wbk.add_worksheet('sheet1')
    sheet.freeze_panes(1, 1)
    columns = [f'{item[0]} {item[1]}' for item in cities_weather_data[0][1]]
    sheet.set_column(1, len(columns), 13)

    sheet.write_row(0, 1, columns, header_style)
    row = 1
    height = 3
    for i in range(len(cities_weather_data)):
        city_weather = cities_weather_data[i]
        if row % 2 == 0:
            row_style = default_style1
        else:
            row_style = default_style0
        weather = city_weather[1]
        col = 0
        last_row = row + height - 1


        sheet.merge_range(first_row=row, last_row=last_row,
                          first_col=col, last_col=col,
                          data=city_weather[0], cell_format=row_style)
        for item in weather:
            d = [item[2], f'{item[3]} {item[4]}', f'{item[6]}~{item[5]}℃']
            col += 1
            sheet.write_column(row, col, d, row_style)
        row += height


class SmtpEmail(object):

    def __init__(self, host, from_addr, password):
        self.from_addr = from_addr
        self.server = smtplib.SMTP_SSL(host, 465)
        self.server.login(from_addr, password)

    def send_email(self, to_addrs, subject, content, atts=None):
        atts = atts or []
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = ','.join(to_addrs)
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        if atts:
            for att_name, att_content in atts:
                attachment = MIMEApplication(att_content)
                attachment["Content-Type"] = 'application/octet-stream'
                attachment.add_header('Content-Disposition', 'attachment',
                                      filename=Header(att_name, 'utf-8').encode())
                msg.attach(attachment)
        self.server.sendmail(self.from_addr, to_addrs, msg.as_string())
        self.server.close()
        return True


def main(write_file=False):
    cities = ['上海', '南京', '杭州', '宁波', '金华', '青岛', '徐州', '济南', '合肥', '苏州', '无锡', '镇江', '马鞍山', '南通', '绍兴', '芜湖']
    data = []
    for city in cities:
        result = Weather2345(city).parsed_data()
        data.append((city, result))

    email_host = 'smtp.qq.com'
    from_addr = ''  # 邮箱地址
    password = ''  # 授权码
    to_addrs = []  # 收件地址列表

    subject = f'【天气预报】{date.today()}'
    content = f'【天气预报】{date.today()}'
    excel_io = BytesIO()
    wbk = xlsxwriter.Workbook(excel_io, {'in_memory': True})
    write_data_2_workbook(wbk, cities_weather_data=data)
    wbk.close()
    excel_io.seek(0)
    atts = [(f'天气预报{date.today()}.xlsx', excel_io.read())]
    smtp_email = SmtpEmail(email_host, from_addr, password)
    smtp_email.send_email(to_addrs=to_addrs, subject=subject, content=content, atts=atts)

    # 写本地文件
    if write_file:
        home_path = os.path.expanduser('~')
        xlsx_name = f'{home_path}/Desktop/天气预报-{str(datetime.date.today())}.xlsx'
        wbk = xlsxwriter.Workbook(filename=xlsx_name)
        write_data_2_workbook(wbk, cities_weather_data=data)
        wbk.close()
    return


if __name__ == '__main__':
    main()
