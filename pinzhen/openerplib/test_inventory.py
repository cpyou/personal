# -*- coding: utf-8 -*-
import openerplib
import logging
import logging.handlers
import sys
import traceback

from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

LOG_FILE = 'test_inventory.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
fmt = '%(asctime)s: %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('test_inventory')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# HOST = 'release.newerp.pinzhen365.com'
# PORT = 80
# DB = 'test_20151116'
# USER = 'admin'
# PASS = 'admin999'

HOST = '127.0.0.1'
PORT = 8069
DB = 'pzfresh_produce_db'
USER = 'admin'
PASS = 'pzfresh818oscg'

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

# product_qtys = [
#     ('电商总仓', 100),  # (仓库名称，盘点单明细实际数量)
#     ('顺德大良店', 150),
#     ('顺德乐从店', 200),
#     ('广州海安店', 220),
#     ('南海万达店', 230),
#     ('顺德容桂店', 240),
#     ('禅城九珑壁店', 260)
# ]
product_qtys = [
    ('电商总仓', 2005),  # (仓库名称，盘点单明细实际数量)
    ('顺德大良店', 2005),
    ('顺德乐从店', 2005),
    ('广州海安店', 2005),
    ('南海万达店', 2005),
    ('顺德容桂店', 2005),
    ('禅城九珑壁店', 2005)
]


def test_inventory():
    model = conn.get_model('stock.inventory')
    line_model = conn.get_model('stock.inventory.line')
    location_model = conn.get_model('stock.location')
    for location_name, product_qty in product_qtys:
        location_ids = location_model.search([('name', '=', location_name)])
        try:
            if location_ids:
                vals = {
                    'filter': 'none',
                    'location_id': location_ids[0],
                }
                logger.info('创建仓库%s的盘点单' % location_name)
                model_id = model.create(vals)
                logger.info('开始盘点')
                model.prepare_inventory([model_id])

                model_val = model.read(model_id, ['line_ids'])
                line_ids = model_val['line_ids']
                logger.info('写盘点单明细实际数量，数量为%s' % len(line_ids))
                line_model.write(line_ids, {'product_qty': product_qty})
                logger.info('审核盘点')
                start_time = datetime.now()
                # model.action_done(model_id)
                model.review_inventory(model_id)
                end_time = datetime.now()
                model_val = model.read(model_id, ['name', 'move_ids'])
                move_num = model_val['move_ids']
                model_name = model_val['name']
                logger.info('仓库%s盘点结束, 盘点单号：%s, 盘点用时:%s, 盘点数量:%s'
                            % (location_name, model_name, str(end_time - start_time), move_num))
                logger.info('盘点单id:%s' % model_id)
                logger.info('\n')
        except (Exception, ):
            message = traceback.format_exc()
            logger.info(message)
    logger.info('程序执行结束\n')

if __name__ == "__main__":
    test_inventory()
