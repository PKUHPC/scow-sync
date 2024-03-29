#!/bin/bash

address=localhost
user=ljz
source=$(pwd)/send_files
destination=$(pwd)/recv_files
max_depth=1
port=22
sshkey_path=/home/ljz/.ssh/id_rsa

# 生成测试文件
mkdir recv_files
mkdir send_files
dd if=/dev/urandom of=$source/file1 bs=1M count=100
cp $source/file1 $source/file2
gzip $source/file2

echo "请使用htop手动查看rsync进程是否开启压缩-z选项, file1需要压缩, file2不需要压缩"
sleep 2

scow-sync -a $address -u $user -s $source -d $destination -m $max_depth -p $port -k $sshkey_path

diff -r "$destination/send_files" $source > /dev/null
if [ $? -eq 0 ]; then
    echo "动态压缩测试完成"
    rm -rf $destination/send_files
    rm -rf $source/*
    echo "删除测试文件完成"
fi