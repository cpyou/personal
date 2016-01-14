# -*- coding: utf-8 -*-
import openerplib
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

HOST = '127.0.0.1'
PORT = 8069
DB = 'pzfresh_produce_db'
USER = 'admin'
PASS = 'pzfresh818oscg'

conn = openerplib.get_connection(hostname=HOST, port=PORT, protocol="jsonrpc", database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)
#     workflow_log = conn.get_model('workflow.logs')
# log_id = workflow_log.create(values)
# log_ids = workflow_log.search([('res_id', '=', '1')])
# log_id = workflow_log.read([id], ['field_name'])
# print log_id
# category_id = category_obj.search([('name', 'like', '骨干')])[0]
# category_obj.write([category_id], {'name': '骨干网络项目'})
# category_obj.create({'name': 'test1', 'name_id': 18})
# category_obj.unlink([23])
workbook = xlsxwriter.Workbook('货品规格规格值数据错误数据.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:E', 15)
bold = workbook.add_format({'bold': 1})
works = [
    '商品名称',
    '商品bn',
    '商品规格备注',
    '商品规格EC id',
    '产品名称',
    '产品货号',
    '产品规格名称',
    '产品规格EC id',
    '产品规格值名称',
    '产品规格值EC id',
    '产品规格值的规格名称',
    '产品规格值的规格EC id',
]

for i in xrange(len(works)):
    worksheet.write(0, i, works[i])
m = 1

model_obj = conn.get_model('ec.goods')
spec_obj = conn.get_model('product.specification')
spec_value_obj = conn.get_model('product.specification.values')
product_obj = conn.get_model('product.product')
model_ids = model_obj.search([], order='id')
goods = model_obj.read(model_ids, ['name', 'bn', 'product_spec_id', 'products'])
for good in goods:
    good_specs = spec_obj.read(good['product_spec_id'][0], ['spec_memo', 'spec_id'])
    products = product_obj.read(good['products'], ['name', 'default_code', 'product_spec_id', 'product_spec_value_id'])
    for product in products:
        product_spec = spec_obj.read(product['product_spec_id'][0], ['spec_memo', 'spec_id'])
        product_spec_value = spec_value_obj.read(product['product_spec_value_id'][0], ['spec_value', 'spec_value_id',
                                                                                       'product_spec_id'])
        spec_value_spec = spec_obj.read(product['product_spec_id'][0], ['spec_memo', 'spec_id'])
        if good_specs['spec_id'] == product_spec['spec_id'] and good_specs['spec_id'] == spec_value_spec['spec_id']:
            continue
        work_data = [
            good['name'],
            good['bn'],
            good_specs['spec_memo'],
            good_specs['spec_id'],
            product['name'],
            product['default_code'],
            product_spec['spec_memo'],
            product_spec['spec_id'],
            product_spec_value['spec_value'],
            product_spec_value['spec_value_id'],
            spec_value_spec['spec_memo'],
            spec_value_spec['spec_id'],
        ]
        for i in xrange(len(work_data)):
            worksheet.write(m, i, work_data[i])
        m += 1
        print m, work_data

workbook.close()
print '完成'