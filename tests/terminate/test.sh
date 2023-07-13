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
dd if=/dev/urandom of=$source/file1 bs=1M count=500
cp $source/file1 $source/file2
mkdir send_files/dir1
cp $source/file1 $source/dir1/file3
cp $source/file1 $source/dir1/file4

scow-sync-start -a $address -u $user -s $source -d $destination -m $max_depth -p $port -k $sshkey_path

flag=0

echo "请观察file1和dir1/file3是否被取消传输"

while true; do
    sleep 0.5
    result=$(scow-sync-query)
    echo $result
    if [[ "$result" = "[]" ]] && [[ $flag -eq 1 ]]; then
        echo "终止传输测试完成"
        rm -rf $destination/send_files
        rm -rf $source/*
        echo "删除测试文件完成"
        exit 0
    fi

    if [[ "$result" != "[]" ]]; then
        flag=1
        if [[ $result == *"file1"* ]]; then
            scow-sync-terminate -a $address -u $user -s $source/file1
        fi
        if [[ $result == *"dir1/file3"* ]]; then
            scow-sync-terminate -a $address -u $user -s $source/dir1/file3
        fi
        echo ""
    fi
done