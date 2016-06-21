-- 电商总仓网络订单商品明细报表
select
     wol.id as id,
     wo.web_name as 订单号,
     wo.order_date + interval '8 hours' as 销售时间,
     wo.stock_order + interval '8 hours' as 发货时间,
     sw.name as 出货仓库,
     rp.name as 业务员,
     pp.default_code as 货号,
     eg.name as 商品名称,
     psv.spec_value as 规格值,
     ps.spec_memo as 规格,
     wol.qty as 数量,
     wol.price_unit as 销售单价,
     wo.amount_total as 实收金额,
     (select wpm.name from web_pay_line wpl left join web_pay_method wpm on wpm.id = wpl.method_id where wpl.pay_id = wo.id LIMIT 1 ) as 支付方式,
     oc.name as 订单来源,
     case wo.state
         when 'draft' then '新建'
         when 'confirmed' then '已确认'
         when 'prestock' then '待发货'
         when 'stock' then '备货中'
         when 'delivery' then '配送中'
         when 'recieved' then '已收货'
         when 'done' then '已完成'
         when 'cancel' then '取消'
         when 'saleafter' then '已申请售后'
         when 'suspend' then '挂起'
         when 'reject' then '拒签'
     end as 状态,
     pc.name as 小类,
     pc2.name as 大类
 from
     web_order_line wol
 join
     web_order wo on wol.order_id = wo.id
 join
     stock_warehouse sw on wo.shipment_warehouse_id = sw.id
 join
     product_product  pp on wol.product_id = pp.id
 join
     product_template  pt on pp.product_tmpl_id = pt.id
 join
     product_category pc on pt.categ_id = pc.id
 left join
     product_category pc2 on pc.parent_id = pc2.id
 join
     ec_goods eg on pt.good = eg.id
 join
     product_specification_values psv on pt.product_spec_value_id = psv.id
 left join
     product_specification ps on pt.product_spec_id = ps.id
 left join 
     res_users ru on wo.user_id = ru.id
 left JOIN res_partner rp on rp.id = ru.partner_id
 left join 
     order_channel oc on wo.order_channel_id = oc.id
 --join 
  --   web_pay_line  wpl on wpl.pay_id = wo.id
 where wo.state not in('cancel','draft') and wo.shipment_warehouse_id =1
     and wo.stock_order >= timestamp '2016-04-01 00:00:00' - interval '8 hours'
     and wo.stock_order < timestamp '2016-05-01 00:00:00' - interval '8 hours'
 order by wo.stock_order 