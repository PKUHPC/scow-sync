'''
Transfer files from local to remote server on SCOW
'''
from io import TextIOWrapper
import os
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from subprocess import Popen, PIPE
import utils
from filequeue import FileQueue, EntityFile
from ssh import SSH


class ScowSync:
    '''
    Transfer files from local to remote server
    '''

    def __init__(self, address, user, sourcepath, destinationpath, max_depth, port, sshkey_path):
        self.address = address
        self.user = user
        self.sourcepath = sourcepath
        self.destinationpath = destinationpath
        self.max_depth = max_depth
        self.port = port
        self.sshkey_path = sshkey_path
        self.compress_list = ['tar', 'zip', 'rar', '7z', 'gz',
                              'bz2', 'xz', 'tgz', 'tbz', 'tb2', 'taz', 'tlz', 'txz'
                              ]
        self.file_queue = FileQueue()
        self.thread_pool = None
        self.raw_string = f'{address} {user} {sourcepath} {destinationpath}'

        self.transfer_id = utils.gen_file_transfer_id(self.raw_string)
        self.base_path = os.path.expanduser('~/scow/.scow-sync')

    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False

    # start rsync
    def __start_rsync(self, cmd, fullpath):
        output_dir_path = os.path.join(
            self.base_path, str(self.transfer_id))
        output_file_path = os.path.join(
            output_dir_path, f'{os.path.basename(fullpath)}.out')
        popen = Popen(cmd, stdout=open(output_file_path, 'a',encoding='utf-8'), stderr=PIPE, universal_newlines=True, shell=True)

        # 等待进程结束
        stdout, stderr = popen.communicate()
        if stderr:
            sys.stderr.write(stderr)

        os.remove(output_file_path)

    # transfer single file
    def __transfer_file(self, filepath):
        print(f'transfering file: {filepath}')
        cmd = None
        src = os.path.join(os.path.split(self.sourcepath)[0], filepath)
        if self.__is_compressed(filepath):
            cmd = f'rsync -a --progress -e \'ssh -p {self.port} -o \'LogLevel=QUIET\'\' \
                    {src} {self.user}@{self.address}:{os.path.join(self.destinationpath, filepath)} \
                    --partial --inplace'
        else:
            cmd = f'rsync -az --progress -e \'ssh -p {self.port} -o \'LogLevel=QUIET\'\' \
                    {src} {self.user}@{self.address}:{os.path.join(self.destinationpath, filepath)} \
                    --partial --inplace'
        self.__start_rsync(cmd, src)
        return

    # transfer directory
    def __transfer_dir(self, dirpath):
        print(f'transfering dir: {dirpath}')
        src = os.path.join(os.path.split(self.sourcepath)[0], dirpath)
        dst = os.path.join(self.destinationpath, os.path.split(dirpath)[0])
        cmd = f'rsync -az --progress  -e \'ssh -p {self.port} -o \'LogLevel=QUIET\'\' \
                {src} {self.user}@{self.address}:{dst} \
                --partial --inplace'

        self.__start_rsync(cmd, src)
        return

    def transfer_files(self):
        '''
        run to transfer files
        '''
        thread_num = min(self.file_queue.add_all_to_queue(
            self.sourcepath, self.max_depth),
            2*cpu_count()+1
        )

        self.thread_pool = ThreadPoolExecutor(
            thread_num, thread_name_prefix='scow-sync')
        while not self.file_queue.empty():
            entity_file: EntityFile = self.file_queue.get()
            if entity_file.isdir:
                if entity_file.depth < self.max_depth:
                    ssh = SSH(self.address, self.user,
                              self.sshkey_path, self.port)
                    string_cmd = f'mkdir -p \
                                 {os.path.join(self.destinationpath, entity_file.subpath)}'
                    ssh.ssh_exe_cmd(cmd=string_cmd)
                else:
                    self.thread_pool.submit(
                        self.__transfer_dir, entity_file.subpath)

            else:
                self.thread_pool.submit(
                    self.__transfer_file, entity_file.subpath)
        self.thread_pool.shutdown()
        os.rmdir(os.path.join(self.base_path, str(self.transfer_id)))
        sys.exit()
