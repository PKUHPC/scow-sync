#!/bin/bash

address=localhost
user=ljz
source=$(pwd)/send_files
destination=$(pwd)/recv_files
max_depth=2
port=2222
sshkey_path=/home/ljz/.ssh/id_rsa

# delete
mkdir recv_files
mkdir $destination/send_files
touch $destination/send_files/file_large_1


# 生成大文件
# mkdir recv_files
mkdir send_files
file_size=105 #MB # 不小于config.py中的SPLIT_THRESHOLD
file_path=$source/file_large_1

dd if=/dev/urandom of=$file_path bs=1M count=$file_size
mkdir $source/dir1
cp $file_path $source/dir1/file_large_2

echo "请手动观察file_large_1没有自动切分，file_large_2进行了自动切分"
sleep 2
scow-sync -a $address -u $user -s $source -d $destination -m $max_depth -p $port -k $sshkey_path

diff -r "$destination/send_files" $source > /dev/null
if [ $? -eq 0 ]; then
    echo "大文件自动切分测试完成，结果正确"
    rm -rf $destination/send_files
    rm -rf $source/*
    echo "删除测试文件完成"
fi