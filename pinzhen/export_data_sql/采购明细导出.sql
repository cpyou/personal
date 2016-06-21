-- 采购明细导出
select 
    po.name 订单号,
--     rp.name 采购员,
    sl.name 收货仓库,
    pt.name 商品名称,
    pp.default_code 货号,
    psv.spec_value 规格值,
    pol.product_qty 数量,
    sum(sm.product_qty) 实收数量,
    pu.name 产品计量单位,
    pol.price_unit 单价,
    po.date_order + INTERVAL '8 hours' 采购日期,
case po.state 
    when 'draft' then '采购订单草稿'
    when 'sent' then '采购订单草稿'
    when 'bid' then '收到投标'
    when 'confirmed' then '等待审批'
    when 'approved' then '已确认采购单'
    when 'except_picking' then '运输异常'
    when 'except_invoice' then '发票异常'
    when 'done' then '完成'
    when 'cancel' then '取消'
end 订单状态
from purchase_order_line pol 
LEFT JOIN purchase_order po on po.id =  pol.order_id
LEFT JOIN product_product pp on pp.id = pol.product_id
LEFT JOIN product_template pt on pt.id = pp.product_tmpl_id
LEFT JOIN product_uom pu ON pu.id = pol.product_uom
join res_users ru on ru.id = po.create_uid
left JOIN res_partner rp on rp.id = ru.partner_id
join product_specification_values psv on psv.id = pol.product_spec_value_id
JOIN stock_location sl ON sl.id = po.location_id
JOIN stock_move sm ON pol.id = sm.purchase_line_id
where po.date_order >= timestamp '2016-01-01 00:00:00' - interval '8 hours'
    AND po.date_order < timestamp '2016-04-01 00:00:00' - interval '8 hours'
    AND sm.state = 'done'
GROUP BY po.name,sl.name,pt.name,pt.name,pp.default_code,psv.spec_value,pol.product_qty,
    pu.name,pol.price_unit,po.date_order,po.state
order by po.date_order