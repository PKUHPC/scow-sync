#!/bin/bash
# usage: sudo bash install.sh

# install rsync, python3, pip3
if [[ -e /etc/os-release ]]; then
    source /etc/os-release
    if [[ $ID == "debian" || $ID == "ubuntu" ]]; then
        apt-get install -y rsync python3 pip3
    elif [[ $ID == "centos" || $ID == "rhel" ]]; then
        yum install -y rsync python3 pip3
    elif [[$ID == "alpine"]]; then
        apk install -y rsync python3 pip3
    else
        echo "Unsupported Linux distribution"
        exit 1
    fi
else
    echo "Unsupported Linux distribution"
    exit 1
fi

# install psutil, paramiko
pip3 install psutil==5.9.4
pip3 install paramiko==3.0.0

# install scow-sync
local_path=$(pwd)
chmod +x $local_path/scow-sync-start
chmod +x $local_path/scow-sync-query
chmod +x $local_path/scow-sync-terminate
ln -s $local_path/scow-sync-start /usr/bin/scow-sync-start # install scow-sync globally by add soft link in /usr/local/bin
ln -s $local_path/scow-sync-query /usr/bin/scow-sync-query
ln -s $local_path/scow-sync-terminate /usr/bin/scow-sync-terminate
ln -s $local_path/scow-sync /usr/bin/scow-sync
chmod +x /usr/bin/scow-sync-start
chmod +x /usr/bin/scow-sync-query
chmod +x /usr/bin/scow-sync-terminate
chmod +x /usr/bin/scow-sync