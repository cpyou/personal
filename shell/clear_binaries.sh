# 循环清理二进制文件
root_dir='/release'
for line in `ls -d $root_dir`
do
    for service_name in `ls $line`
    do
        ls -dt $root_dir/$service_name/* | grep $service_name- | tail -n +12
        ls -dt $root_dir/$service_name/* | grep $service_name- | tail -n +12 | xargs -d '\n' -r rm --
    done
done