#!/bin/bash

# usage: bash test.sh 查询进度 bash test.sh delete 删除测试文件
address=localhost
user=ljz
source=$(pwd)/send_files
destination=$(pwd)/recv_files
max_depth=2
port=2222
sshkey_path=/home/ljz/.ssh/id_rsa
if [ $# -eq 0 ]; then

    # 生成测试文件
    mkdir recv_files
    mkdir send_files
    dd if=/dev/urandom of=$source/file1 bs=1M count=100
    cp $source/file1 $source/file2
    mkdir $source/dir1
    cp $source/file1 $source/dir1/file3
    cp $source/file1 $source/dir1/file4
    mkdir $source/dir1/dir2
    cp $source/file1 $source/dir1/dir2/file5
    cp $source/file1 $source/dir1/dir2/file6
    echo "生成测试文件完成"


    scow-sync-start -a $address -u $user -s $source -d $destination -m $max_depth -p $port -k $sshkey_path

    while true; do
        sleep 1
        scow-sync-query
        echo ""
    done
fi
# delete
if [ "$1" = "delete" ]; then
    rm -rf $destination/send_files
    rm -rf $source/*
    echo "删除测试文件完成"
fi