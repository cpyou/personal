-- 总仓库存信息
WITH t AS (
    SELECT
        pp.default_code 货号,
        pp.ean13 条码,
        pt.name 商品名称,
        sum(sq.qty) 数量,
        sw.name 仓库,
        sl.name 仓库库位,
        sq.location_id 库位
    FROM stock_quant sq
    right join product_product pp on pp.id = sq.product_id
    join product_template pt on pt.id = pp.product_tmpl_id
    left join stock_warehouse sw on sw.lot_stock_id = sq.location_id
    left join stock_location  sl on sl.id = sq.location_id
    left join product_category pc1 on pc1.id = pt.categ_id
    left join product_category pc2 on pc2.id = pc1.parent_id
    where sw.name = '电商总仓' AND pc2.name = '肉品类'
    group by pp.default_code, pt.name, pp.ean13, sw.name, sq.location_id, sl.name
    order by sw.name
)
SELECT * FROM t  WHERE t.数量 > 0;

