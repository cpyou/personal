# -*- coding: utf-8 -*-
import openerplib
import xlsxwriter
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# HOST = 'erp.pzfresh.com'
# PORT = 80
# DB = 'pzfresh_produce_db'
# USER = 'admin'
# PASS = 'wlcmima159632'

HOST = '127.0.0.1'
PORT = 8069
DB = 'pzfresh_produce_db'
USER = 'admin'
PASS = 'admin999'

start_time = '2015-12-31 00:00:00'
end_time = '2015-12-31 23:59:59'


def adjust_time_use_hours(input_time, hours):
    time1 = datetime.datetime.strptime(input_time[:19], '%Y-%m-%d %H:%M:%S')
    time2 = time1 + datetime.timedelta(hours=hours)
    time3 = time2.strftime('%Y-%m-%d %H:%M:%S')
    return time3


conn = openerplib.get_connection(hostname=HOST, port=PORT, protocol="jsonrpc", database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)

header_data = [
    ('盘点单号', 'name'),
    ('产品名称', 'product_name'),
    ('规格值', 'spec_value'),
    ('规格', 'spec'),
    ('分类', 'category'),
    ('成本', 'standard_price'),
    ('系统数量', 'theoretical_qty'),
    ('盘点后数量', 'product_qty'),
    ('盘点后库存价值', 'inventory_amount'),
    ('差异数', 'diff_qty'),
    ('差异金额', 'diff_amount'),
    ('盘点单时间', 'date'),
    ('生效时间', 'write_date'),
    # ('备注', ''),
]
headers = [line[0] for line in header_data]
work_keys = [line[1] for line in header_data]

workbook = xlsxwriter.Workbook('盘点差异表(%s~%s).xlsx' % (start_time, end_time))

start_time = adjust_time_use_hours(start_time, -8)
end_time = adjust_time_use_hours(end_time, -8)

template_obj = conn.get_model('product.template')
product_obj = conn.get_model('product.product')
inventory_obj = conn.get_model('stock.inventory')
location_obj = conn.get_model('stock.location')
inventory_line_obj = conn.get_model('stock.inventory.line')
spec_value_obj = conn.get_model('product.specification.values')


location_ids = location_obj.search([('usage', '=', 'internal')], order='id')
location_vals = location_obj.read(location_ids, ['name'])
for location_val in location_vals:
    work_data = []
    work_products = []
    inventory_ids = inventory_obj.search([('location_id', '=', location_val['id']),
                                          ('date', '>', start_time),
                                          ('date', '<', end_time),
                                          ('state', '=', 'done')], order='write_date')
    if inventory_ids:
        worksheet = workbook.add_worksheet(location_val['name'])
        worksheet.set_column('A:E', 15)
        bold = workbook.add_format({'bold': 1})

        for i in xrange(len(headers)):
            worksheet.write(0, i, headers[i])
        row = 1

        print len(inventory_ids)
        for inventory_id in inventory_ids:
            inventory_val = inventory_obj.read(inventory_id, ['name', 'line_ids', 'date', 'write_date'])
            for line_id in inventory_val['line_ids']:
                line = inventory_line_obj.read(line_id, ['product_id', 'theoretical_qty', 'product_qty'])
                product_val = product_obj.read(line['product_id'][0], ['product_tmpl_id', 'standard_price'])
                template_val = template_obj.read(product_val['product_tmpl_id'][0], ['product_spec_value_id',
                                                                                     'product_spec_id',
                                                                                     'categ_id'])

                product_name = line['product_id'][1]
                if product_name in work_products:
                    line_data = work_data[work_products.index(product_name)]
                    line_data.update({
                        'name': '%s,%s' % (line_data['name'], inventory_val['name']),
                        'product_qty': line_data['product_qty'] + (line['product_qty'] - line['theoretical_qty']),
                        'date': adjust_time_use_hours(inventory_val['date'], 8),
                        'write_date': adjust_time_use_hours(inventory_val['write_date'], 8),
                    })
                else:
                    line_data = {
                        'name': inventory_val['name'],
                        'standard_price': product_val['standard_price'],
                        'spec_value': template_val['product_spec_value_id'][1],
                        'spec': template_val['product_spec_id'][1],
                        'category': template_val['categ_id'][1],
                        'product_name': product_name,
                        'theoretical_qty': line['theoretical_qty'],
                        'product_qty': line['product_qty'],
                        'date': adjust_time_use_hours(inventory_val['date'], 8),
                        'write_date': adjust_time_use_hours(inventory_val['write_date'], 8),
                    }
                    work_data.append(line_data)
                    work_products.append(line_data['product_name'])
                print row, line_data
        for line_data in work_data:
            line_data['diff_qty'] = line_data['product_qty'] - line_data['theoretical_qty']
            line_data['diff_amount'] = line_data['diff_qty'] * line_data['standard_price']
            line_data['inventory_amount'] = line_data['product_qty'] * line_data['standard_price']

            for key in work_keys:
                worksheet.write(row, work_keys.index(key), line_data[key])
            print row, line_data
            row += 1
workbook.close()
print '完成'
#     workflow_log = conn.get_model('workflow.logs')
    # log_id = workflow_log.create(values)
    # log_ids = workflow_log.search([('res_id', '=', '1')])
    # log_id = workflow_log.read([id], ['field_name'])
    # print log_id
    # category_id = category_obj.search([('name', 'like', '骨干')])[0]
    # category_obj.write([category_id], {'name': '骨干网络项目'})
    # category_obj.create({'name': 'test1', 'name_id': 18})
    # category_obj.unlink([23])
# model = conn.get_model('web.to.erp')
# obj = 'web.order'
# method = 'write'
# vals = {
#     'model': 'web.order',
#     'method': 'write',
#     'domain': [
#         ('web_name', '=', '150602092713298')],
#     'args': {
#         'state': 'done'
#     }
# }
# apply_ids = model.synchronous_method(vals)


# model = conn.get_model('pay.order.sync')
# apply_ids = model.pay_order_sync()
