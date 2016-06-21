-- 加工单信息-多对一
SELECT
    msp.name 加工单号,
    sw.name 门店,
    pt.name 成品,
    pp.default_code 货号,
    msp.product_uom_qty 数量,
    pu.name 计量单位,
    msp.create_date 制单日期,
    CASE msp.state
        WHEN 'draft' THEN '草稿'
        WHEN 'confirm' THEN '待加工'
        WHEN 'done' THEN '完成'
        WHEN 'cancel' THEN '取消'
        ELSE msp.state
    END 状态
FROM mrp_simple_production msp
JOIN stock_warehouse sw ON sw.id = msp.warehouse_id
JOIN product_product pp ON pp.id = msp.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
JOIN product_specification_values psv ON psv.id = pt.product_spec_value_id
JOIN product_uom pu ON pu.id = msp.product_uom
WHERE msp.create_date >= '2016-01-01'
    AND msp.create_date < '2016-04-01'
ORDER BY msp.create_date
