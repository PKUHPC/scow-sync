'''
Transfer files from local to remote server on SCOW
'''
import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from subprocess import Popen, PIPE
from filequeue import FileQueue, EntityFile
from ssh import SSH


class ScowSync:
    '''
    Transfer files from local to remote server
    '''

    def __init__(self, address, user, sshpassword, sourcepath, destinationpath):
        self.address = address
        self.user = user
        self.sshpassword = sshpassword
        self.sourcepath = sourcepath
        self.destinationpath = destinationpath
        self.compress_list = ['.tar', '.zip', '.rar', '.7z', '.gz',
                              '.bz2', '.xz', '.tgz', 'tbz', 'tb2', 'taz', 'tlz', 'txz'
                              ]
        self.file_queue = FileQueue()
        self.thread_pool = None

    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False

    # transfer single file
    def __transfer_file(self, filepath):
        print(f'transfering file: {filepath}')
        cmd = None
        src = os.path.join(os.path.split(self.sourcepath)[0], filepath)
        if self.__is_compressed(filepath):
            cmd = f'sshpass -p {self.sshpassword} rsync -a --progress \
                    {src} {self.user}@{self.address}:{os.path.join(self.destinationpath, filepath)} \
                    --partial --inplace'
        else:
            cmd = f'sshpass -p {self.sshpassword} rsync -az --progress \
                    {src} {self.user}@{self.address}:{os.path.join(self.destinationpath, filepath)} \
                    --partial --inplace'
        with Popen(cmd, stdout=PIPE, universal_newlines=True, shell=True) as popen:
            while popen.poll() is None:
                line = popen.stdout.readline()
                print(f'transfering file: {filepath} {line.strip()}')
        return

    def transfer_files(self):
        '''
        run to transfer files
        '''
        thread_num = min(self.file_queue.add_all_to_queue(
            self.sourcepath),
            2*cpu_count()+1
        )

        self.thread_pool = ThreadPoolExecutor(
            thread_num, thread_name_prefix='scowsync')
        while not self.file_queue.empty():
            entity_file: EntityFile = self.file_queue.get()
            if entity_file.isdir:
                ssh = SSH(self.address, self.user, self.sshpassword)
                string_cmd = f'mkdir -p {os.path.join(self.destinationpath, entity_file.subpath)}'
                ssh.ssh_exe_cmd(cmd=string_cmd)
            else:
                self.thread_pool.submit(
                    self.__transfer_file, entity_file.subpath)
        self.thread_pool.shutdown()
