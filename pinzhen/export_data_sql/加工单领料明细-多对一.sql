-- 加工单领料明细-多对一
SELECT
    msp.name 加工单号,
    pt.name 原料名称,
    pp.default_code 货号,
    msl.product_uom_qty 数量,
    pu.name 计量单位,
    pc.name 分类
FROM mrp_simple_line msl
JOIN mrp_simple_production msp ON msp.id = msl.product_order
JOIN product_product pp ON pp.id = msl.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
JOIN product_uom pu ON pu.id = msl.product_uom
JOIN product_category pc on pc.id = msl.categ_id
WHERE msp.create_date >= '2016-01-01'
    AND msp.create_date < '2016-04-01'
ORDER BY msp.create_date