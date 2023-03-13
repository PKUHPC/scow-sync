#!/bin/bash
# install scow-sync globally by add soft link in /usr/local/bin
# usage: sudo bash install.sh
pip install paramiko==3.0.0
local_path=$(pwd)
chmod +x $local_path/scow-sync
ln -s $local_path/scow-sync /usr/local/bin/scow-sync
chmod +x /usr/local/bin/scow-sync