'''
query thr progress of file transfered
'''
from argparse import ArgumentParser
import os
import sys
import subprocess
import psutil




class PidArgsParser:
    '''
    Parse pid
    '''
    def __init__(self):
        self.parser = ArgumentParser(
            description='query the progress of file transfer'
        )
    def get_args_parser(self) -> ArgumentParser:
        '''
        Get the argument parser
        @return: the argument parser
        '''
        # fid
        self.parser.add_argument(
            '-f', '--files_transfer_id',
            type=int,
            help='the id of the file transfer this time'
        )

        # pid
        self.parser.add_argument(
            '-p', '--pid',
            type=int,
            help='the pid of the file transfer this time'
        )      
        return self.parser

if __name__ == '__main__':
    args = PidArgsParser().get_args_parser().parse_args()
    fid = args.files_transfer_id
    pid = args.pid

    filename = f'./tmp/{fid}.out'
    process = psutil.Process(pid)

    if os.path.exists(filename):
        cmd = ["tail", "-f", filename]
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while popen.poll() is None and process.is_running():
            stdout = popen.stdout
            if stdout:
                output = stdout.readline()
                if output:
                    sys.stdout.write(output.decode().strip())
                    sys.stdout.write('\n')
                    sys.stdout.flush()
        # 最后删除文件
        os.remove(filename)

    else:
        sys.stdout.write('No transfer temp file')
        exit(1)
