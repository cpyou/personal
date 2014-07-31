#!/bin/bash
start_time=`date +%F-%H%M`
OF="/mnt/backup/pufa_stj/openerp/$start_time-pufa_db.bak"
PGLOGDIR="/mnt/backup/pufa_stj/log/pufa_db_bak.log"
echo '开始清理数据库'  `date +%F-%H:%M:%S`
vacuumdb pufa_db
echo '清理数据库完成，开始备份数据库'  `date +%F-%H:%M:%S` >> $PGLOGDIR
pg_dump pufa_db > "$OF"
echo '完成数据库备份，开始压缩备份文件'  `date +%F-%H:%M:%S` >> $PGLOGDIR
pbzip2 "$OF"
echo '压缩备份文件完成，开始传输备份文件到远程服务器' `date +%F-%H:%M:%S` >> $PGLOGDIR
scp "$OF.bz2" 10.190.1.101:/mnt/backup/pufa_stj/openerp/
echo '备份代码' `date +%F-%H:%M:%S` >> $PGLOGDIR
bak_addons=/mnt/backup/pufa_stj/openerp/$start_time-addons
cp -r /home/openerp/bde/project/PUFA/stj/addons/  $bak_addons
scp -r $bak_addons 10.190.1.101:/mnt/backup/pufa_stj/openerp/
finish_time=`date +%F-%H:%M:%S`
echo $finish_time "备份成功！" >> $PGLOGDIR
echo "备份数据库名：$OF" >> $PGLOGDIR
echo "备份代码名：$bak_addons" >> $PGLOGDIR

echo "删除大于60天的备份" >> $PGLOGDIR
# 删除大于60天的备份
 find /mnt/backup/pufa_stj/openerp/* -maxdepth 0 -mtime +61 -exec rm -r {} \;
# 删除大于20天的备份
 ssh 10.190.1.101 'find /mnt/backup/pufa_stj/openerp/* -maxdepth 0 -mtime +21 -exec rm -r {} \;'
echo '完成' `date +%F.%H:%M:%S`
echo "" >> $PGLOGDIR

scp -r /mnt/backup/pufa_stj/log/ 10.190.1.101:/mnt/backup/pufa_stj/
