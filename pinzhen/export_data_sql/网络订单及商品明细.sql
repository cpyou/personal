-- 网络订单及商品明细sql.txt
select
    wo.name 单号,
    wo.web_name 网单号,
    rp.name 客户,
    rp2.name 配送地址,
    wo.delivery_date + interval '8 hours' 配送日期,
    wo.order_date + interval '8 hours' 下单时间,
    wo.stock_order + interval '8 hours' 实际发货时间,
    wo.amount_total 实收总金额,
    wo.cost 订单成本,
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
    pp.default_code 货号,
    pt.name 商品名称,
    wol.name 说明,
    wol.qty 数量,
    pu.name 单位,
    wol.price_origin 原价,
    wol.price_unit 单价,
    wol.discount "折扣(%)",
    wol.subtotal 小计
from web_order_line wol
join web_order wo on wo.id = wol.order_id
join res_partner rp on rp.id = wo.partner_id 
join res_partner rp2 on rp2.id = wo.address_id 
join product_product pp on pp.id = wol.product_id
join product_template pt on pt.id = pp.product_tmpl_id
join product_uom pu on pu.id = pt.uom_id
where wo.order_date >= timestamp '2016-04-01 00:00:00' - interval '8 hours'
    and wo.order_date < timestamp '2016-05-01 00:00:00' - interval '8 hours'
    AND rp.name in ('jd001', 'jd002', 'jd003', 'yaguanjia001')
ORDER BY rp.name, wo.order_date
--       and wo.shipment_warehouse_id = 1
