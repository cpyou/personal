-- 模型权限组用户数据
select
    im.name 模型描述,
    im.model 模型,
    rg.name 组,
    ima.perm_read 组读权限,
    ima.perm_write 组写入权限,
    ima.perm_create 组创建权限,
    ima.perm_unlink 组删除访问许可,
    ru.login 账号,
    rp.name 用户名
from ir_model im
join ir_model_access ima on ima.model_id =  im.id
join res_groups rg on rg.id = ima.group_id
join res_groups_users_rel rgur on rgur.gid = rg.id
join res_users ru on ru.id = rgur.uid
join res_partner rp on rp.id = ru.partner_id
where model in ('product.template', 'stock.picking', 'sale.order', 'web.order',
'return.apply', 'mrp.simple.production', 'stock.inventory', 'res.partner', 'purchase.order')
ORDER BY im.model,rg.name