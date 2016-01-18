# -*- coding: utf-8 -*-
import openerplib
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8090
DB = ''
USER = ''
PASS = ''

conn = openerplib.get_connection(hostname=HOST, port=PORT, database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)

#     workflow_log = conn.get_model('workflow.logs')
#     log_id = workflow_log.create(values)
#     log_ids = workflow_log.search([('res_id', '=', '1')])
#     log_id = workflow_log.read([id], ['field_name'])
#     print log_id
#     category_id = category_obj.search([('name', 'like', '骨干')])[0]
#     category_obj.write([category_id], {'name': '骨干网络项目'})
#     category_obj.create({'name': 'test1', 'name_id': 18})
#     category_obj.unlink([23])
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


model = conn.get_model('product.template')
quant_model = conn.get_model('stock.quant')

num = 1000
start_time = datetime.now()
for i in range(num):
    # vals = {
    #     'name': 'cpu%s' % i,
    #     'type': 'product',
    # }
    # product_id = model.create(vals)
    print i
    quant_vals = {
        'product_id': i + 1,
        'location_id': 12,
        'qty': 10,
    }
    quant_model.create(quant_vals)
end_time = datetime.now()
print str(end_time - start_time)
