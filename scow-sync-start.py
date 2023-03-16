'''
Start a file transfer asynchronously
'''
import sys
from subprocess import Popen, PIPE
from argsparser import ArgsParser


if __name__ == '__main__':
    args = ArgsParser().get_args_parser().parse_args()
    cmd = f'python3 scow-sync.py -a {args.address} -u {args.user} -s {args.source} -d {args.destination} -m {args.max_depth} -p {args.port} -k {args.sshkey_path}'
    popen = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    sys.stdout.write(str(popen.pid))

