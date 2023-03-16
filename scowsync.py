'''
Transfer files from local to remote server on SCOW
'''
import os
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from subprocess import Popen, PIPE
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

    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False

    # output filepath, progress, speed and time of json into stdout
    def __parse_rsync_output(self, line, filepath):
        parts = line.split()
        progress = parts[1]
        speed = parts[2]
        time = parts[3]
        sys.stdout.write(json.dumps({"filepath":filepath, 'progress': progress, 'speed': speed, 'time': time}))
        sys.stdout.write("\n")

    # output transfer progress to stdout
    def __output_progress(self, popen, filepath):
        while popen.poll() is None:
            stdout = popen.stdout
            if stdout is not None:
                line = stdout.readline()
                if "%" in line:
                    self.__parse_rsync_output(line,filepath)


    # transfer single file
    def __transfer_file(self, filepath):
        # print(f'transfering file: {filepath}')
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
        # Popen(cmd, stdout=PIPE, universal_newlines=True, shell=True)
        popen = Popen(cmd, stdout=PIPE, universal_newlines=True, shell=True)
        self.__output_progress(popen, src)
        return

    # transfer directory
    def __transfer_dir(self, dirpath):
        # print(f'transfering dir: {dirpath}')
        src = os.path.join(os.path.split(self.sourcepath)[0], dirpath)
        dst = os.path.join(self.destinationpath, os.path.split(dirpath)[0])
        cmd = f'rsync -az --progress  -e \'ssh -p {self.port} -o \'LogLevel=QUIET\'\' \
                {src} {self.user}@{self.address}:{dst} \
                --partial --inplace'

        # Popen(cmd, stdout=PIPE, universal_newlines=True, shell=True)
        popen = Popen(cmd, stdout=PIPE, universal_newlines=True, shell=True)
        self.__output_progress(popen, src)
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
