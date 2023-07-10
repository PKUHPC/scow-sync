#!/bin/bash

# usage: sudo bash install.sh
# install rsync, python3, pip3
if [ $# -eq 0 ]; then
    if [[ -e /etc/os-release ]]; then
        source /etc/os-release
        if [[ $ID == "debian" || $ID == "ubuntu" ]]; then
            apt-get install -y rsync python3 pip3
        elif [[ $ID == "centos" || $ID == "rhel" ]]; then
            yum install -y rsync python3 pip3
        elif [[ $ID == "alpine" ]]; then
            apk add -y rsync python3 pip3
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
    dir_path=$local_path/scow_sync
    chmod +x $dir_path/scow-sync-start
    chmod +x $dir_path/scow-sync-query
    chmod +x $dir_path/scow-sync-terminate
    ln -s $dir_path/scow-sync-start /usr/bin/scow-sync-start # install scow-sync globally by add soft link in /usr/local/bin
    ln -s $dir_path/scow-sync-query /usr/bin/scow-sync-query
    ln -s $dir_path/scow-sync-terminate /usr/bin/scow-sync-terminate
    ln -s $dir_path/scow-sync /usr/bin/scow-sync
    chmod +x /usr/bin/scow-sync-start
    chmod +x /usr/bin/scow-sync-query
    chmod +x /usr/bin/scow-sync-terminate
    chmod +x /usr/bin/scow-sync
fi

# config the shebang
if [ "$1" = "update" ]; then
    # 读取SHEBANG_PATH变量
    SHEBANG_PATH=$(python3 -c "from scow_sync import config; print(config.SHEBANG_PATH)")
    # 更新scow-sync脚本的shebang行
    sed -i "1s|.*|#!$SHEBANG_PATH|" ./scow_sync/scow-sync
    # 更新scow-sync-start脚本的shebang行
    sed -i "1s|.*|#!$SHEBANG_PATH|" ./scow_sync/scow-sync-start
    # 更新scow-sync-query脚本的shebang行
    sed -i "1s|.*|#!$SHEBANG_PATH|" ./scow_sync/scow-sync-query
    # 更新scow-sync-terminate脚本的shebang行
    sed -i "1s|.*|#!$SHEBANG_PATH|" ./scow_sync/scow-sync-terminate
fi