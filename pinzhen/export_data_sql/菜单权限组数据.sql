-- 菜单权限组用户数据
-- 菜单名称:售后申请单
select
    ium.name 模型描述,
    rg.name 组,
    ru.login 账号,
    rp.name 用户名
from ir_ui_menu ium
JOIN ir_ui_menu_group_rel iumgr ON ium.id = iumgr.menu_id
join res_groups rg on iumgr.gid = rg.id
join res_groups_users_rel rgur on rgur.gid = rg.id
join res_users ru on ru.id = rgur.uid
join res_partner rp on rp.id = ru.partner_id
where ium.name = '售后申请单' AND ru.active = TRUE
ORDER BY ium.name,rg.name