#!/bin/bash

address=localhost
user=ljz
source=$(pwd)/send_files
destination=$(pwd)/recv_files
max_depth=2
port=2222
sshkey_path=/home/ljz/.ssh/id_rsa


# 生成测试文件
mkdir recv_files
mkdir send_files
dd if=/dev/urandom of=$source/file1 bs=1M count=10
cp $source/file1 $source/file2
mkdir $source/dir1
cp $source/file1 $source/dir1/file3
cp $source/file1 $source/dir1/file4
mkdir $source/dir1/dir2
cp $source/file1 $source/dir1/dir2/file5
cp $source/file1 $source/dir1/dir2/file6
echo "生成测试文件完成"


scow-sync -a $address -u $user -s $source -d $destination -m $max_depth -p $port -k $sshkey_path

diff -r "$destination/send_files" $source > /dev/null
if [ $? -eq 0 ]; then
    echo "并行传输测试完成，结果正确"
    rm -rf $destination/send_files
    rm -rf $source/*
    echo "删除测试文件完成"
fi