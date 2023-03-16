# Scow-Sync
A file transfer system backend on SCOW

## Install

### dependencies
- python3
 
- pip3

- paramiko 3.0.0

### install globally
Clone the repository in a directory that all users have access to, then execute`sudo bash install.sh`

## Usage
Usage:

```bash
python3 scow-sync-start [-h] [-a ADDRESS] [-u USER] [-s SOURCE] [-d DESTINATION] [-p PORT] [-k SSHKEY_PATH]
```

Optional arguments:

  `-h, --help`  show this help message and exit

  `-a ADDRESS, --address ADDRESS` address of the server

  `-u USER, --user USER`  username for logging in to the server

  `-s SOURCE, --source SOURCE`  path to the source file or directory

  `-d DESTINATION, --destination DESTINATION` path to the destination directory
  
  `-p PORT, --port PORT`  port of the server

  `-k SSHKEY_PATH, --sshkey-path PATH`  path to id_rsa file
  