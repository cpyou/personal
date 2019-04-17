# -*- coding: UTF-8 -*-
# =================================================
#      language       ： Python3.7
#      IDLE           :  pycharm
#      Library needed ： re,requests.urlib
#      Date           :  17/04/2019
# =================================================
import re
import datetime
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
        r = re.compile(r'<p><strong>([^<]+)\(<font.*?>([^<]+)</font>\).*?<b>([^<]+)</b><i><font class="blue">' \
                       '([^<]+)</font>～<font class="red">([^<]+)</font><br.*?((?<=>)[^<]+)</i>', re.M | re.S)
        result = re.findall(r, text)
        fbsj = 'From:2345天气预报'
        print('  -----' + self.city + '天气预报' + '(未来' + str(len(result)) + '天）' + fbsj + '-----')
        print('-' * 60)
        for p in result:
            p0, p1, p2, p3, p4, p5 = p
            print("  {0:^6}\t {1:^2}\t{2:{6}<6}\t{3:{6}<4}\t{4:{6}^3}\t{5:{6}<6}".format(p0, p1, p2, p3, p4,
                                                                                         p5.replace(' ', ''),
                                                                                         chr(12288)))
        print('-' * 60)
        return result


def write_data_2_xlsx(filename=None, cities_weather_data=None):
    filename = filename or 'test.xlsx'
    cities_weather_data = cities_weather_data or []
    wbk = xlsxwriter.Workbook(filename=filename)
    sheet = wbk.add_worksheet('sheet1')
    columns = [f'{item[0]} {item[1]}' for item in cities_weather_data[0][1]]

    sheet.write_row(0, 1, columns)
    row = 1
    height = 3
    for city_weather in cities_weather_data:
        weather = city_weather[1]
        col = 0
        last_row = row + height - 1
        sheet.merge_range(first_row=row, last_row=last_row, first_col=col, last_col=col, data=city_weather[0])
        for item in weather:
            d = [item[2], f'{item[3]}~{item[4]}', item[5]]
            col += 1
            sheet.write_column(row, col, d)
        row += height
    wbk.close()


if __name__ == '__main__':
    cities = ['上海']
    data = []
    for city in cities:
        result = Weather2345(city).parsed_data()
        data.append((city, result))

    xlsx_name = f'~/Desktop/天气预报-{str(datetime.date.today())}.xlsx'
    write_data_2_xlsx(filename=xlsx_name, cities_weather_data=data)
