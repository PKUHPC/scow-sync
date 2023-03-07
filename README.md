# scow-sync
A file transfer system backend on SCOW

## dependencies
- python3

- paramiko 3.0.0

## Usage
Usage: scow-sync.py [-h] [-a ADDRESS] [-u USER] [-p PASSWORD] [-s SOURCE] [-d DESTINATION]

File transfer system for SCOW

Optional arguments:

  -h, --help            show this help message and exit

  -a ADDRESS, --address ADDRESS
                        address of the server

  -u USER, --user USER  username for logging in to the server

  -p PASSWORD, --password PASSWORD
                        password for logging in to the server

  -s SOURCE, --source SOURCE
                        path to the source file or directory

  -d DESTINATION, --destination DESTINATION
                        path to the destination directory
