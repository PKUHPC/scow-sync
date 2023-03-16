'''
Start a file transfer asynchronously
'''
import sys
import hashlib
from subprocess import Popen
from argsparser import ArgsParser

if __name__ == '__main__':
    args = ArgsParser().get_args_parser().parse_args()
    cmd = f'python3 scow-sync.py -a {args.address} -u {args.user} -s {args.source} -d {args.destination} -m {args.max_depth} -p {args.port} -k {args.sshkey_path}'
    
    # 此次传输的重定向文件，使用hashlib生成
    hash_object = hashlib.md5(cmd.encode())
    hash_value = int.from_bytes(hash_object.digest(), byteorder='big')
    modulus = 10**9 + 7;
    unique_id = hash_value % modulus

    popen = Popen(cmd, shell=True, stdout=open(f'./tmp/{unique_id}.out', 'w'))

    sys.stdout.write(str(unique_id))
    exit(0)
