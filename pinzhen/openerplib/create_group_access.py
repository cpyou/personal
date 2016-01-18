# -*- coding: utf-8 -*-
import openerplib

HOST = '127.0.0.1'
PORT = 8069
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


model = conn.get_model('ir.model')
group_model = conn.get_model('res.groups')
access_model = conn.get_model('ir.model.access')
apply_ids = model.search([('osv_memory', '=', False)])
model_vals = model.read(apply_ids, ['id', 'name', 'modules'])
group_id = group_model.create({'name': '只读组'})

for model_val in model_vals:
    if model_val['modules'] != 'base':
        vals = {
            'group_id': group_id,
            'model_id': model_val['id'],
            'name': model_val['name'],
            'perm_read': True,
        }
        access_model.create(vals)

