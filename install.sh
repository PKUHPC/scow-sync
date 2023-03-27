#!/bin/bash
# install scow-sync globally by add soft link in /usr/local/bin
# usage: sudo bash install.sh
pip3 install psutil==5.9.4
pip3 install paramiko==3.0.0
local_path=$(pwd)
chmod +x $local_path/scow-sync-start
chmod +X $local_path/scow-sync-query
ln -s $local_path/scow-sync-start /usr/bin/scow-sync-start
ln -s $local_path/scow-sync-query /usr/bin/scow-sync-query
ln -s $local_path/scow-sync /usr/bin/scow-sync
chmod +x /usr/bin/scow-sync-start
chmod +x /usr/bin/scow-sync-query
mkdir /tmp
mkdir /tmp/scow-sync
touch /tmp/scow-sync/scow-sync.out
touch /tmp/scow-sync/scow-sync.err
chmod 777 /tmp/scow-sync
chmod 777 /tmp/scow-sync/scow-sync.out
chmod 777 /tmp/scow-sync/scow-sync.err
