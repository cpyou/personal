-- 网络订单汇总数据导出
SELECT
  sw.name 出货仓库,
  wo.name 单号,
  wo.web_name 网单号,
  rp.name 客户,
  rp2.name 收货人,
  rp2.city 城市,
  rcs.name 省份,
  wo.delivery_date + interval '8 hours' 配送日期,
  wo.order_date + interval '8 hours' 下单时间,
  wo.stock_order + interval '8 hours' 实际发货时间,
  wo.amount_total 实收总金额,
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
  oc.name 订单渠道,
  wo.buyer_memo 买家备注,
  wo.seller_memo 卖家备注
FROM web_order wo
JOIN stock_warehouse sw ON sw.id = wo.shipment_warehouse_id
JOIN res_partner rp ON rp.id = wo.partner_id
JOIN res_partner rp2 ON rp2.id = wo.address_id
LEFT JOIN res_country_state rcs on rcs.id = rp2.state_id
JOIN order_channel oc ON oc.id = wo.order_channel_id
WHERE wo.order_date >= timestamp '2016-01-01 00:00:00' - interval '8 hours'
  AND wo.order_date < timestamp '2016-04-01 00:00:00' - interval '8 hours'
ORDER BY wo.order_date
