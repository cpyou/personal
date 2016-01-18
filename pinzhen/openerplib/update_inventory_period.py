# -*- coding: utf-8 -*-
import openerplib
import logging
import logging.handlers
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

LOG_FILE = 'update_inventory_period.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
fmt = '%(asctime)s: %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('update_inventory_period')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


HOST = '127.0.0.1'
PORT = 8069
DB = ''
USER = ''
PASS = ''

conn = openerplib.get_connection(hostname=HOST, port=PORT, database=DB, login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)

# workflow_log = conn.get_model('workflow.logs')
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


def update_period():
    inventory_model = conn.get_model('stock.inventory')
    period_model = conn.get_model('account.period')
    inventory_ids = inventory_model.search([('period_id', '=', False)])
    inventory_vals = inventory_model.read(inventory_ids, ['name', 'date'])
    for inventory_val in inventory_vals:
        period_ids = period_model.search([('date_start', '<=', inventory_val['date'][:10]),
                                          ('date_stop', '>=', inventory_val['date'][:10])])
        period_val = period_model.read(period_ids, ['name'])
        inventory_model.write([inventory_val['id']], {'period_id': period_ids[0]})
        logger.info('盘点单：%s，盘点单时间：%s，修改评估期间：%s' %
                    (inventory_val['name'], inventory_val['date'], period_val[0]['name']))
    logger.info('程序执行结束\n')

if __name__ == "__main__":
    update_period()
