#!/bin/bash
backup_server=10.100.1.166
DB='pms_db'
start_time=`date +%F-%H%M`
OF="/mnt/backup/pfgj_stj/openerp/$start_time-ipm_pfgj.bak"
attach_dir=/home/openerp/.local/share/Odoo/filestore/pms_db
PGLOGDIR="/mnt/backup/pfgj_stj/log/ipm_pfgj_bak.log"

echo `date +%F-%H:%M:%S` '开始清理数据库' | tee -a $PGLOGDIR
vacuumdb $DB
echo `date +%F-%H:%M:%S` '清理数据库完成，开始备份数据库'  | tee -a $PGLOGDIR
pg_dump $DB > "$OF"
echo `date +%F-%H:%M:%S` '完成数据库备份，开始压缩备份文件'  | tee -a $PGLOGDIR
pbzip2 "$OF"
echo `date +%F-%H:%M:%S` '压缩备份文件完成，开始传输备份文件到远程服务器' | tee -a $PGLOGDIR
scp "$OF.bz2" $backup_server:/mnt/backup/pfgj_stj/openerp/

echo `date +%F-%H:%M:%S` '备份代码' | tee -a $PGLOGDIR
bak_addons=/mnt/backup/pfgj_stj/openerp/$start_time-addons
cp -r ~/dev/ipm/addons/  $bak_addons
scp -r $bak_addons $backup_server:/mnt/backup/pfgj_stj/openerp/

echo `date +%F-%H:%M:%S` '备份附件'  | tee -a $PGLOGDIR
bak_attach_dir=/mnt/backup/pfgj_stj/openerp/$start_time-attach-pms_db
cp -r $attach_dir $bak_attach_dir
scp -r $bak_attach_dir $backup_server:/mnt/backup/pfgj_stj/openerp/

finish_time=`date +%F-%H:%M:%S`
echo $finish_time "备份成功！" | tee -a $PGLOGDIR
echo "备份数据库名：$OF" | tee -a $PGLOGDIR
echo "备份代码名：$bak_addons" | tee -a $PGLOGDIR
echo "备份附件：$bak_attach_dir" | tee -a $PGLOGDIR

echo "删除大于60天的备份" | tee -a $PGLOGDIR
# 删除大于60天的备份
find /mnt/backup/pfgj_stj/openerp/* -maxdepth 0 -mtime +61 -exec rm -r {} \;
# 删除大于20天的备份
ssh $backup_server 'find /mnt/backup/pfgj_stj/openerp/* -maxdepth 0 -mtime +21 -exec rm -r {} \;'
echo `date +%F-%H:%M:%S` '完成' | tee -a $PGLOGDIR
echo "" >> $PGLOGDIR

scp -r /mnt/backup/pfgj_stj/log/ $backup_server:/mnt/backup/pfgj_stj/
