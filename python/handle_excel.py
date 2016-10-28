# -*- coding: utf-8 -*-
import xlrd
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


data = xlrd.open_workbook('/Users/chenpuyu/Downloads/品类.xls')
table = data.sheets()[0]
nrows = table.nrows
categories = {}
for i in range(nrows):
    if i != 0:
        categories[table.row_values(i)[1]] = table.row_values(i)[2]

category_keys = categories.keys()

l3 = [i for i in category_keys if len(i) == 3]
l5 = [i for i in category_keys if len(i) == 5]
l5_parent = list(set([i[:3] for i in category_keys if len(i) == 5]))
l7 = [i for i in category_keys if len(i) == 7]
l7_parent = list(set([i[:5] for i in category_keys if len(i) == 7]))
l9 = [i for i in category_keys if len(i) == 9]
l9_parent = list(set([i[:7] for i in category_keys if len(i) == 9]))
print(list(set(l5).difference(set(l7_parent))))
print(list(set(l7).difference(set(l9_parent))))
print(len(category_keys), len(l3), len(l5_parent), len(l5), len(l7_parent), len(l7), len(l9_parent), len(l9))

workbook = xlsxwriter.Workbook('品类分组.xlsx')
worksheet = workbook.add_worksheet()
headers = [
    '一级',
    '二级',
    '三级',
    '四级',
]
row = 0
for i in range(len(headers)):
    worksheet.write(row, i, headers[i])
l9.sort()
for i in l9:
    row += 1
    key1 = i[:3]
    key2 = i[:5]
    key3 = i[:7]
    worksheet.write(row, 0, key1 + categories[key1])
    worksheet.write(row, 1, key2 + categories[key2])
    worksheet.write(row, 2, key3 + categories[key3])
    worksheet.write(row, 3, i + categories[i])
for i in list(set(l7).difference(set(l9_parent))):
    row += 1
    worksheet.write(row, 0, i[:3] + categories[i[:3]])
    worksheet.write(row, 1, i[:5] + categories[i[:5]])
    worksheet.write(row, 2, i[:7] + categories[i[:7]])
workbook.close()
