#!/bin/bash

address=pku
user=root
source=$(pwd)/send_files
destination=/root/file-transfer/file-test
max_depth=2
port=22
sshkey_path=/home/ljz/.ssh/id_rsa


# 生成测试文件
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

find $source -type f -not -name "local_checksums.txt" -exec sha1sum {} \; | awk '{print $1}' | sort > $source/local_checksums.txt

ssh -p $port -i $sshkey_path $user@$address "find $destination/send_files -type f -exec sha1sum {} \; | awk '{print $1}' | cut -f1 -d' ' | sort > $destination/send_files/remote_checksums.txt"

rsync -av -e "ssh -p $port -i $sshkey_path" $user@$address:$destination/send_files/remote_checksums.txt $source 

diff $source/remote_checksums.txt $source/local_checksums.txt > /dev/null
if [ $? -eq 0 ]; then
    echo "远程并行传输测试完成，结果正确"
    rm -rf $source/*
    ssh -p $port -i $sshkey_path $user@$address rm -rf $destination/*
    echo "删除测试文件完成"
fi
