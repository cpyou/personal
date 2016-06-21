-- 销售订单汇总数据导出
SELECT
  sw.name 仓库,
  CASE so.pz_order_type
    WHEN 'p2b' THEN '国际采购p2b'
    WHEN 'office' THEN '办公室接待'
    WHEN 'VIP' THEN '大客户'
    WHEN 'sale_raw' THEN '营销领用'
    WHEN 'gf_sale' THEN '广佛营销中心'
    WHEN 'sz_sale' THEN '深圳营销中心'
    WHEN 'wangguanjia' THEN  '旺管家'
    WHEN 'baoli' THEN '保利'
    WHEN 'BD_Business' THEN 'BD商务合作组'
    WHEN 'other' THEN '其他'
    ELSE so.pz_order_type
  END 订单来源,
  so.name 单号,
  rp.name 客户
FROM sale_order so
JOIN stock_warehouse sw ON sw.id = so.warehouse_id
JOIN res_partner rp ON rp.id = so.partner_id