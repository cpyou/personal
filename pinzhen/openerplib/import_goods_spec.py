#!env python
# -*- coding: utf-8 -*-
import xlrd
import openerplib

HOST = '127.0.0.1'
PORT = 8069
DB = 'zhixian'
USER = 'admin'
PASS = 'admin'

conn = openerplib.get_connection(hostname=HOST, port=PORT, database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)
model = conn.get_model('product.specification')

data = xlrd.open_workbook('品珍鲜活-金蝶系统商品列表.xlsx')
table = data.sheets()[0]
nrows = table.nrows  # 获取行数
for i in range(nrows):
    vals = {}
    row_values = table.row_values(i)
    vals['spec_id'] = row_values[0]
    model.create(vals)
