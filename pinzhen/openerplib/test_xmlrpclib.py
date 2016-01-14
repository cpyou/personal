# -*- coding: utf-8 -*-
import xmlrpclib

url = 'http://112.74.83.141:8069'
db = 'pzfresh'
username = 'admin'
password = '123'
# url = 'http://127.0.0.1:8069'
# db = 'zhixian'
# username = 'admin'
# password = 'admin'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
a = models.execute_kw(db, uid, password, 'eshop.to.odoo', 'synchronous_method', [{'a'}, {}])
print a