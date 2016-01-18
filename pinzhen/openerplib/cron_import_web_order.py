# -*- coding: utf-8 -*-
import openerplib

HOST = '127.0.0.1'
PORT = 8069
DB = ''
USER = ''
PASS = ''

conn = openerplib.get_connection(hostname=HOST, port=PORT, protocol="jsonrpc", database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)
model = conn.get_model('eshop.backend')
apply_ids = model.scheduler_import_sale_orders()
