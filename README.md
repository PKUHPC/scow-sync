# Scow-Sync
A file transfer system backend on SCOW

## Install

### dependencies
- python3 (Make sure the path is `usr/bin/python3`. If not, change the first line of `scow-sync` to the correct path)

- paramiko 3.0.0

### install globally
Execute `sudo bash install.sh`, this will install the script globally by create a symbolic link in `/usr/bin/`.

## Usage
Usage:

```bash
scow-sync [-h] [-a ADDRESS] [-u USER] [-s SOURCE] [-d DESTINATION] [-p PORT] [-k SSHKEY_PATH]
```

Optional arguments:

  `-h, --help`  show this help message and exit

  `-a ADDRESS, --address ADDRESS` address of the server

  `-u USER, --user USER`  username for logging in to the server

  `-s SOURCE, --source SOURCE`  path to the source file or directory

  `-d DESTINATION, --destination DESTINATION` path to the destination directory
  
  `-p PORT, --port PORT`  port of the server

  `-k SSHKEY_PATH, --sshkey-path PATH`  path to id_rsa file
  