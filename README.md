# Scow-Sync
A file transfer system tool on SCOW

## Install

### dependencies

- python3
 
- pip3

- paramiko 3.0.0

- psutil 5.9.4 

- rsync >= 3.1.0

### install globally

Clone the repository in a directory that sudoer have access to, then execute`sudo bash install.sh`. 

## Usage

### start

You can use the following command for transfer, but the command will return immediately and write the transfer ID(for your query, you can see next) and process ID to stdout. If you first execute the command, it will create the directory `~/scow/.scow-sync` to store the transfer information including the transferring log and error log.

```bash
scow-sync-start [-h] [-a ADDRESS] [-u USER] [-s SOURCE] [-d DESTINATION] [-p PORT] [-k SSHKEY_PATH]
```

Optional arguments:

  `-h, --help`  show this help message and exit

  `-a ADDRESS, --address ADDRESS` address of the server

  `-u USER, --user USER`  username for logging in to the server

  `-s SOURCE, --source SOURCE`  path to the source file or directory

  `-d DESTINATION, --destination DESTINATION` path to the destination directory
  
  `-p PORT, --port PORT`  port of the server

  `-k SSHKEY_PATH, --sshkey_path PATH`  path of private key

### query

You can use the following command to view the real-time transfer process.

```bash
scow-sync-query
```

It will return an array of json object like:

```json
[{
  "recvAddress":recv_address, 
  "filePath": file_path, 
  "transferSize": transfer_size,
  "progress": progress, 
  "speed": speed, 
  "leftTime": time
}...]
```





  