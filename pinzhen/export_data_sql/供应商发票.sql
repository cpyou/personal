-- 供应商发票
SELECT
    rp.name 供应商,
    ai.date_invoice 发票日期,
    ai.number 编号,
    rp2.name 负责人,
    ai.date_due 到期日期,
    ai.origin 源单据,
    rc.name 币别,
    ai.residual 结转余额,
    ai.amount_untaxed 小计,
    ai.amount_total 总计,
    CASE ai.state
        WHEN 'draft' THEN '草稿'
        WHEN 'proforma' THEN '形式发票'
        WHEN 'proforma2' THEN '形式发票'
        WHEN 'open' THEN '打开'
        WHEN 'paid' THEN '已付'
        WHEN 'cancel' THEN '已取消'
        ELSE ai.state
    END 状态,
    ai.create_date 创建日期
FROM account_invoice ai
JOIN res_partner rp ON ai.partner_id = rp.id
LEFT JOIN res_users ru ON ai.user_id = ru.id
LEFT JOIN res_partner rp2 ON ru.partner_id = rp2.id
JOIN res_currency rc ON ai.currency_id = rc.id
WHERE ai.type = 'in_invoice'
ORDER BY ai.create_date