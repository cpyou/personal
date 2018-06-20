db_back_dir=''
dest_dir=''
host='{IP}'
file_name=`ssh root@$host ls -t $db_back_dir|head -1`
scp root@$host:$db_back_dir$file_name $dest_dir
echo $file_name
