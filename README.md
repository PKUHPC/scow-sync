# scow-sync
A file transfer system backend on SCOW

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

## Performance vs rsync
```sh
time sshpass -p Gfacljz001028 rsync -az --progress ~/file-test/* root@47.113.184.248:/root --partial --inplace
sending incremental file list
file1G
  1,073,741,824 100%   11.55MB/s    0:01:28 (xfr#1, to-chk=8/9)
test1/
test1/file1G-1
  1,073,741,824 100%   11.59MB/s    0:01:28 (xfr#2, to-chk=4/9)
test1/test1.4/
test1/test1.4/file1G-4
  1,073,741,824 100%   11.43MB/s    0:01:29 (xfr#3, to-chk=2/9)
test2/
test2/file1G-2
  1,073,741,824 100%   11.39MB/s    0:01:29 (xfr#4, to-chk=1/9)
test3/
test3/file1G-3
  1,073,741,824 100%   11.67MB/s    0:01:27 (xfr#5, to-chk=0/9)

real    7m24.201s
user    4m30.628s
sys     0m8.339s
```

```sh
time python3 test.py
transfering file: file-test/test1/file1G-1
transfering file: file-test/test1/test1.4/file1G-4
transfering file: file-test/test3/file1G-3
transfering file: file-test/test2/file1G-2
transfering file: file-test/file1G

real    7m25.086s
user    4m21.619s
sys     0m9.211s
```