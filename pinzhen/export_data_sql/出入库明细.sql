-- 出入库明细
SELECT
  sm.name 说明,
  sp.name 相关单号,
  sm.origin 源单据,
  spt.name 分拣类型,
  pt.name 产品,
  pp.default_code 货号,
  sm.product_uom_qty 数量,
  pu.name 计量单位,
  sl.name 源库位,
  sl2.name 目的库位,
  sm.date + interval '8 hours' 日期,
  sm.date_expected + interval '8 hours' 预计日期,
  CASE sm.state
    WHEN 'draft' THEN '新建'
    WHEN 'cancel' THEN '取消'
    WHEN 'waiting' THEN '等待其他调拨'
    WHEN 'confirmed' THEN '等待可用'
    WHEN 'assigned' THEN '可用'
    WHEN 'done' THEN '完成'
    ELSE sm.state
  END 状态
FROM stock_move sm
JOIN stock_picking sp ON sp.id = sm.picking_id
JOIN stock_picking_type spt ON spt.id = sm.picking_type_id
JOIN product_product pp ON pp.id = sm.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
JOIN product_uom pu ON pu.id = sm.product_uom
JOIN stock_location sl ON sl.id = sm.location_id
JOIN stock_location sl2 ON sl2.id = sm.location_dest_id
where sm.date >= timestamp '2016-01-01 00:00:00' - interval '8 hours'
    AND sm.date < timestamp '2016-04-01 00:00:00' - interval '8 hours'
order by sm.date
