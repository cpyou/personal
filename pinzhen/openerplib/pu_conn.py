# -*- coding: utf-8 -*-
import openerplib
import xmlrpclib
import json

HOST = '127.0.0.1'
PORT = 8069
DB = 'pzfresh_produce_db'
USER = 'admin'
PASS = 'admin999'

conn = openerplib.get_connection(hostname=HOST, port=PORT, protocol="jsonrpc", database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)
model = conn.get_model('return.apply')

# re = model.product_sync_pos()
# search = [('id', '>', 99244),('id', '<', 99259),('active','=',True)]
# re  = model.handle_pruduct_data(search)

# domain = [('sync_times','=',0),('state','in',('paid','invoiced','done'),('id','=',9))]
# model.category_sync()
re = model.apply_api()


#
# HOST = '120.24.92.42'
# PORT = 8069
# DB = 'test_20150923'
# USER = 'admin'
# PASS = 'pzfresh818oscg'
#
# conn = openerplib.get_connection(hostname=HOST, port=PORT, protocol="jsonrpc", database=DB, login=USER, password=PASS)
#
# print conn.login, conn.password
# conn.check_login()
# print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)
# model = conn.get_model('product.product')
#
# ids = model.search([('product_tmpl_id', '=', 92615)])
#
# print ids

#
# ids = models.execute_kw(db, uid, password,
#     'res.partner', 'search',
#     [[['is_company', '=', True], ['customer', '=', True]]],
#     {'limit': 1})
# [record] = models.execute_kw(db, uid, password,
#     'res.partner', 'read', [ids])

# ids = model.search([('id', '=', '98851')])
# data = model.read(ids)
# print ids
# print data

    #workflow_log = conn.get_model('workflow.logs')
    # log_id = workflow_log.create(values)
    # log_ids = workflow_log.search([('res_id', '=', '1')])
    # log_id = workflow_log.read([id], ['field_name'])
    # print log_id
    # category_id = category_obj.search([('name', 'like', '骨干')])[0]
    # category_obj.write([category_id], {'name': '骨干网络项目'})
    # category_obj.create({'name': 'test1', 'name_id': 18})
    # category_obj.unlink([23])

