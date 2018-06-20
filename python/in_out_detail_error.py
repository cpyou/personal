#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


conn = MySQLdb.connect(
    host='',
    port=3306,
    user='',
    passwd='',
    # db='ctcdb_ck_test',
)

goodid = 137606  # 商品库存id
start_time = '2017-12-11 11:26:43'
end_time = '2017-12-11 11:26:43'
# 使用cursor()方法获取操作游标
cursor = conn.cursor()

# 主仓进销存明细
where_str = ''
if goodid:
    if where_str:
        where_str += ' AND  ciod_good_id = %s' % goodid
    else:
        where_str += ' ciod_good_id = %s' % goodid

if start_time:
    if where_str:
        where_str += ' AND  ciod_change_date >= %s' % start_time
    else:
        where_str += ' ciod_change_date >= %s' % start_time

if end_time:
    if where_str:
        where_str += ' AND  ciod_change_date <= %s' % end_time
    else:
        where_str += ' ciod_change_date <= %s' % end_time

stock_sql = """
SELECT
    ciod_id 主键ID,
    DATE_FORMAT(ciod_change_date, '%%Y-%%m-%%d %%H:%%i:%%S')  出入库时间,
    ciod_type 类型,
    ciod_change_num 出入库折算散装数量,
    ciod_pStart_num 期初数量,
    ciod_pEnd_num 期末数量,
    ciod_bill_id 单据ID,
    ciod_good_id 商品ID,
    ciod_warehouse_id 仓库ID,
    ciod_city_id 城市ID,
    ciod_bill_name 单据名称,
    ciod_number_id 单据单号,
    ciod_remark 备注,
    DATE_FORMAT(createdAt, '%%Y-%%m-%%d %%H:%%i:%%S') 创建时间,
    DATE_FORMAT(updatedAt, '%%Y-%%m-%%d %%H:%%i:%%S') 修改时间
FROM ctcdb_ck_test.center_in_out_details
WHERE %s ciod_change_date = '2017-12-11 11:26:43';
""" % where_str

# 使用execute方法执行SQL语句
cursor.execute(stock_sql)

workbook = xlsxwriter.Workbook('仓库进销存明细.xlsx')
worksheet = workbook.add_worksheet()

headers = [d[0] for d in cursor.description]
row = 0

worksheet.write_row(row, 0, headers)

# 使用 fetchone() 方法获取一条数据
# print [d.name for i, d in enumerate(cursor.description)]
data = cursor.fetchall()
for d in data:
    row += 1
    worksheet.write_row(row, 0, d)

workbook.close()

# 财务进销存明细
where_str = ''
if goodid:
    if where_str:
        where_str += ' AND  GoodId = %s' % goodid
    else:
        where_str += ' GoodId = %s' % goodid

if start_time:
    if where_str:
        where_str += ' AND  iDate >= %s' % start_time
    else:
        where_str += ' iDate >= %s' % start_time

if end_time:
    if where_str:
        where_str += ' AND  iDate <= %s' % end_time
    else:
        where_str += ' iDate <= %s' % end_time
account_sql = """
SELECT
    id 主键ID,
    DATE_FORMAT(iDate, '%%Y-%%m-%%d %%H:%%i:%%S') 出入库时间,
    type 类型,
    inPrice '入库单价-散装单价',
    inNum 入库折算散装数量,
    inAmount 入库单价,
    outNum 出库折算散装数量,
    outAmount 出库折算金额,
    outPrice 出库成本,
    pStartNum 期初数量,
    pStartAmount 期初金额,
    pEndNum 期末数量,
    pEndAmount 期末总价,
    remark 备注,
    DATE_FORMAT(createdAt, '%%Y-%%m-%%d %%H:%%i:%%S') 创建时间,
    DATE_FORMAT(updatedAt, '%%Y-%%m-%%d %%H:%%i:%%S') 更新时间,
    GoodId 商品库存id,
    ReceiptId 入库单ID,
    WarehouseId 仓库id,
    StoreId 店铺id,
    SupplierId 第三方id,
    StoreGoodsOrderId ,
    ProviderId 供货商ID,
    netPrice 当前成本单价,
    TransferApplyId 调拨单ID,
    ReceiveGoodsOrderId 收货单ID,
    ReturnGoodsOrderId 退货单ID,
    numberId 对应单号,
    BranchWarehouseId 前置仓ID
FROM ctcdb_new_test.in_out_details
%s
""" % where_str

for d in data:
    ciod_change_date = d[1]  # 出入库时间
    ciod_change_num = d[3]  # 出入库折算散装数量
    ciod_pStart_num = d[4]  # 期初数量
    ciod_pEnd_num = d[5]  # 期末数量
    where_args = (ciod_change_date, ciod_change_num, ciod_pStart_num, ciod_pEnd_num)
    d_where_str = """
    AND iDate = '%s'
    AND inNum = %d
    AND pStartNum = %d
    AND pStartAmount = %d
    """ % where_args
    account_sql += d_where_str
    # 使用execute方法执行SQL语句
    cursor.execute(account_sql)
    account_io_data = cursor.fetchall()
    if len(account_io_data) != 1:
        for aio_d in account_io_data:
            pass
# 使用execute方法执行SQL语句
# cursor.execute(account_sql)

workbook = xlsxwriter.Workbook('财务进销存明细.xlsx')
worksheet = workbook.add_worksheet()

headers = [d[0] for d in cursor.description]
row = 0

worksheet.write_row(row, 0, headers)

# 使用 fetchone() 方法获取一条数据
# print [d.name for i, d in enumerate(cursor._obj.description)]
data = cursor.fetchall()
for d in data:
    row += 1
    worksheet.write_row(row, 0, d)

workbook.close()

# 关闭游标
cursor.close()

# 关闭数据库连接
conn.close()

