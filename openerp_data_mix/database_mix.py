# -*- coding: utf-8 -*-
'''
    本程序核心思想是先生成数据字典，然后对数据库内容进行全局搜索替换，
    其中，主要数据字典生成自动根据项目名称和用户名，自动生成；
    可在字典“private_dict”自定义需要替换的内容，
'''
import openerplib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("/home/openerp/code/v7/server")
# import openerp
# import openerp.addons
# import threading
# import openerp.tools

import random
import copy

# random.randint(1, 100)
# HOST = '192.168.0.194'
HOST = '192.168.1.114'
PORT = 8069
DB = ''
USER = ''
PASS = ''
# db = openerp.sql_db.db_connect(DB)
# threading.current_thread().dbname = DB
# pool = openerp.pooler.get_pool(DB)
# cr = db.cursor()

conn = openerplib.get_connection(hostname=HOST, port=PORT, database=DB,
    login=USER, password=PASS)

print conn.login, conn.password
conn.check_login()
print "Logged in as %s(uid:%d)" % (conn.login, conn.user_id)


def main(conn):
#     workflow_log = conn.get_model('workflow.logs')
    # log_id = workflow_log.create(values)
    # log_ids = workflow_log.search([('res_id', '=', '1')])
    # log_id = workflow_log.read([('res_id', '=', '1')])
    # print log_id
    # category_id = category_obj.search([('name', 'like', '骨干')])[0]
    # category_obj.write([category_id], {'name': '骨干网络项目'})
    # category_obj.create({'name': 'test1', 'name_id': 18})
    # category_obj.unlink([23])
    model = 'stj.document.project'
#     mix_res = set_mix_dict(conn, model)
    mix_res = {}

    # 自定义替换内容
    private_dict = {
                    u'上海': u'北京',
                    u'浦': u'华',
                    u'迪斯尼': u'游乐园',
                    u'商飞': u'社区医疗',
                    u'康桥镇': u'剑桥镇',
                    u'张江镇': u'长江镇',
                    u'花木街道': u'花城街道',
                    u'陆家嘴城管办': u'西沙城管办',
                    }
    user_dict = set_mix_user_dict(conn)
    mix_res.update(user_dict)
    mix_res.update(private_dict)

    module_list = ['stj_base','stj_document', 'stj_fund', 'stj_repo', 'stj_account']
    model_list = get_handle_model_name(conn, module_list)
#     mix_model_data(cr, conn, model, mix_res)

#     db = openerp.sql_db.db_connect(DB)
#     cr = db.cursor()

    for model1 in model_list:
        mix_model_data(conn, model1, mix_res)
    mix_res1 = set_mix_dict(conn, model)
    for model1 in model_list:
        mix_model_data(conn, model1, mix_res1)
    

    clear_attachment(conn)  # 清理附件
#     cr.close()
    print '完成'


def set_mix_dict(conn, model, list_ids=None):
    '''
       随机变换名称，并隐藏部分内容,生成混淆字典
       注意：需配置postfix参数
    '''
    model_obj = conn.get_model(model)
    if type(list_ids) == list:
        project_ids = list_ids
    else:
        project_ids = model_obj.search([])
    names = model_obj.read(project_ids, ['name'])
    project_names = [name['name'] for name in names]
    mix_res = {}
    l = []

    postfix = '.'  # 指定命名后缀，避免变换名称后名称唯一性错误

    deep_project_names = copy.deepcopy(project_names)
    for deep_project_name in deep_project_names:
        num = random.randint(0, len(project_names) - 1)
        project_name = project_names[num]
        # 加*处理名称
        if len(project_name) > 6:
            project_name = project_name.replace(project_name[3:6], '***')
        if len(project_name) > 12:
            project_name = project_name.replace(project_name[9:12], '***')
        project_name = project_name + postfix
        i = 1
        if project_name in l:
            project_name = '%s$%s' % (project_name, i)
            i += 1
        mix_res[deep_project_name] = project_name
        l.append(project_name)
        project_names.remove(project_names[num])
    print '混淆字典数目：%s' % len(mix_res)
    return mix_res


def mix_model_data(conn, model, mix_res):
    '''
        根据混淆字典，替换model内的内容
    '''
    # 忽略出问题的模块 原因未查出
    if model in ['stj.document.distribute', 'stj.document.signed']:
        return

    model_obj = conn.get_model(model)
    try:
        model_ids = model_obj.search([], order='id')
        for model_id in model_ids:
            print model_id
            vals = {}
            results = model_obj.read([model_id], [])
    #             print len(results[0])
            for k, v in results[0].iteritems():
    #                 print '%s %s' % (k, v)
                if type(v) in (str, unicode):
                    for mix_k, mix_v in mix_res.iteritems():
    #                         print '%s %s' % (mix_k, mix_v)
                        if k in vals:
                            v = vals[k]
                        if mix_k in v:
                            v = v.replace(mix_k, mix_v)
                            vals[k] = v
            if vals:
                try:
#                     model_table = model.replace('.', '_')
#                     vals_str = ""
#                     for val_k, val_v in vals.iteritems():
#                         vals_str = "%s='%s'," % (val_k, val_v)
#                     vals_str = vals_str[:-1]
#                     cr.execute('update %s set %s where id=%s' % (model_table, vals_str, model_id))
#                     cr.commit()
                    model_obj.write([model_id], vals)
                    print 'model:%s; id:%s; value:%s' % (model, model_id, vals)
                except:
                    print '出现异常：%s,model_id:%s, %s' % (model, model_id, model_obj)
    except:
        print 'model出现异常：%s, %s' % (model, model_obj)


def get_handle_model_name(conn, module_list):
    '''
        获取需要的model，返回包含model名的列表
    '''
    model_obj = conn.get_model('ir.model')
    model_ids = model_obj.search([])
    model_list = []
    for model_id in model_ids:
        results = model_obj.read([model_id], ['model', 'modules'])
        modules = results[0]['modules']
        if modules in module_list:
            model = results[0]['model']
            model_list.append(model)
    model_list.append('res.partner')  # 添加用户表
    print 'model数目：%s' % len(model_list)
    return model_list


def clear_attachment(conn):
    model_obj = conn.get_model('ir.attachment')
    attachment_ids = model_obj.search([], order='id')
    for attachment_id in attachment_ids:
        data = model_obj.read([attachment_id], ['db_datas', 'datas_fname', 'name'])
        file_postfix = data[0]['name'][-3:]
        if file_postfix in ['pdf', 'txt', 'xls', 'png', 'jpg', 'doc']:
            with open ('./测试.%s' % file_postfix, 'rb') as myfile:
                bna = myfile.read()
                model_obj.write([attachment_id], {'db_datas': bna.encode('base64')})
                print 'ok_' + str(attachment_id)
        else:
            with open ('./测试.pdf', 'rb') as myfile:
                bna = myfile.read()
                datas_fname = data[0]['datas_fname'][:-4] + '.pdf'
                name = data[0]['name'][:-4] + '.pdf'
                model_obj.write([attachment_id], {'db_datas': bna.encode('base64'), 'datas_fname': datas_fname, 'name': name})
                print 'ok_' + str(attachment_id)
    print '清理附件完成'


def set_mix_user_dict(conn):
    res = {
           u'赵红丽': u'赵红',
           u'冯俊杰': u'冯俊',
           u'张宇鹏': u'张宇',
           u'魏庆泰': u'卫青',
           u'王红玉': u'王红',
           u'郑航': u'郑和',
           u'周焰': u'周岩',
           u'郭晓晖': u'郭辉',
           u'黄郁青': u'黄小青',
           u'李培彦': u'李彦宏',
           u'陈新': u'陈大庆',
           u'张延红': u'张挺',
           u'张雷': u'陈布雷',
           u'杨晓冬': u'汤晓冬',
           u'黄娴': u'黄淑',
           u'朱剑能': u'朱剑刚',
           u'刘婕': u'班婕',
           u'刘浩宇': u'徐浩宇',
           u'张文革': u'张文化',
           u'翁涌': u'张勇',
           u'王向阳': u'杨过',
           }
    model_obj = conn.get_model('res.users')
    model_ids = model_obj.search([])
    for model_id in model_ids:
        name = model_obj.read([model_id], ['name'])[0]['name']
        if name in res:
            continue
        if len(name) == 3:
            name1 = name.replace(name[1], u'小')
        elif len(name) == 2:
            name1 = '%s%s%s' % (name[0], u'小', name[1])
        else:
            name1 = name
        res[name] = name1
    return res


if __name__ == '__main__':
    main(conn)
