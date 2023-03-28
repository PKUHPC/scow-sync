#!/bin/bash
# install scow-sync globally by add soft link in /usr/local/bin
# usage: sudo bash install.sh
pip3 install psutil==5.9.4
pip3 install paramiko==3.0.0
if [[ -e /etc/os-release ]]; then
    source /etc/os-release
    if [[ $ID == "debian" || $ID == "ubuntu" ]]; then
        apt-get install -y rsync
    elif [[ $ID == "centos" || $ID == "rhel" ]]; then
        yum install -y rsync
    elif [[$ID == "alpine"]]; then
        apk install -y rsync
    else
        echo "Unsupported Linux distribution"
        exit 1
    fi
else
    echo "Unsupported Linux distribution"
    exit 1
fi
local_path=$(pwd)
chmod +x $local_path/scow-sync-start
chmod +x $local_path/scow-sync-query
ln -s $local_path/scow-sync-start /usr/bin/scow-sync-start
ln -s $local_path/scow-sync-query /usr/bin/scow-sync-query
ln -s $local_path/scow-sync /usr/bin/scow-sync
chmod +x /usr/bin/scow-sync-start
chmod +x /usr/bin/scow-sync-query
chmod +x /usr/bin/scow-sync