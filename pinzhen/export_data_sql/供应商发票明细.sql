-- 供应商发票明细
DROP AGGREGATE IF EXISTS array_accum(anyelement);
CREATE AGGREGATE array_accum (anyelement)
(
    sfunc = array_append,
    stype = anyarray,
    initcond = '{}'
);

CREATE OR REPLACE FUNCTION _group_concat(text, text)
RETURNS text AS $$
SELECT CASE
WHEN $2 IS NULL THEN $1
WHEN $1 IS NULL THEN $2
ELSE $1 operator(pg_catalog.||) ',' operator(pg_catalog.||) $2
END
$$ IMMUTABLE LANGUAGE SQL;

DROP AGGREGATE IF EXISTS group_concat(text);
CREATE AGGREGATE group_concat (
BASETYPE = text,
SFUNC = _group_concat,
STYPE = text
);

SELECT
    ai.origin 源单据,
    ai.number 编号,
    pp.default_code 产品货号,
    pt.name 产品名称,
    ail.name 说明,
    aa.name 科目,
    aac.name 资产类别,
    ail.quantity 数量,
    pu.name 计量单位,
    ail.price_unit 单价,
    group_concat(tax.name),
    ail.price_subtotal 本位币金额
FROM account_invoice_line ail
LEFT JOIN account_invoice ai ON ail.invoice_id = ai.id
LEFT JOIN product_product pp ON ail.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN account_account aa ON ail.account_id = aa.id
LEFT JOIN account_asset_category aac ON ail.asset_category_id = aac.id
LEFT JOIN product_uom pu ON ail.uos_id = pu.id
LEFT JOIN account_invoice_line_tax ailt ON ail.id = ailt.invoice_line_id
LEFT JOIN account_tax tax ON ailt.tax_id = tax.id
WHERE ai.type = 'in_invoice'
GROUP BY ai.id,ai.number,pp.default_code,pt.name,ail.id,aa.name,aac.name,
    pu.name,pu.name