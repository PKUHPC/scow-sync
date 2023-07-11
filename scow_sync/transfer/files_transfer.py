'''
Transfer files from local to remote server on SCOW
'''
import os
import sys
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from subprocess import Popen, PIPE
import config
from utils import ssh, gen_file_transfer_id
from transfer import files_queue


class FilesTransfer:
    '''
    Transfer files from local to remote server
    '''

    def __init__(self, address, user, src_path, dst_path, max_depth, port, sshkey_path):
        # args
        self.address = address
        self.user = user
        self.src_path = src_path
        self.dst_path = dst_path
        self.max_depth = max_depth
        self.port = port
        self.sshkey_path = sshkey_path
        # class value
        self.compress_list = ['tar', 'zip', 'rar', '7z', 'gz',
                              'bz2', 'xz', 'tgz', 'tbz', 'tb2', 
                              'taz', 'tlz', 'txz']
        self.output_path = config.OUTPUT_PATH
        # split large files
        self.split_dict = {}
        self.split_lock = threading.Lock() # mutex for accessing split_dict
        # parallel files transfer
        self.file_queue = files_queue.FileQueue()
        self.thread_pool = None
        # identifies the transfer process
        self.raw_string = f'{address} {user} {src_path} {dst_path}'
        self.transfer_id = gen_file_transfer_id(self.raw_string)
        # ssh
        self.ssh = ssh.SSH(self.address, self.user, self.sshkey_path, self.port)

    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False

    # split large file
    def __split_large_file(self, file_full_path) -> str:
        '''
        split large file locally, returns the path of the temporary directory where the split large file is stored
        @return: the local temp dir path like '{file_full_path}_sstemp'
        '''
        print(f'spliting large file: {file_full_path}')

        temp_dir_path = f'{file_full_path}_sstemp'
        os.makedirs(temp_dir_path, 0o700)

        file_name = os.path.basename(file_full_path)

        cmd = f'split -b {config.SPLIT_CHUNK_SIZE}M {file_full_path} {temp_dir_path}/{file_name}_'
        popen = Popen(cmd, stderr=PIPE, universal_newlines=True, shell=True)

        _, stderr = popen.communicate()

        if stderr:
            sys.stderr.write(stderr)
            return None  # type: ignore
        
        # compute num of sub files
        count = 0
        file_list = os.listdir(temp_dir_path)
        count = len(file_list)
        # update thread shared dict
        split_element = {'count': count, 'current': 0}

        self.split_lock.acquire()
        self.split_dict.update({temp_dir_path: split_element})
        self.split_lock.release()

        return temp_dir_path

    # merge files
    def __merge_files(self, dst_temp_file_prefix, dst_file_full_path):
        
        cmd_cat = f'cat {dst_temp_file_prefix}_* > {dst_file_full_path}'
        self.ssh.ssh_exe_cmd(cmd_cat)
        
        dst_temp_dir_path: str = os.path.split(dst_temp_file_prefix)[0]
        cmd_rm = f'rm -rf {dst_temp_dir_path}'
        self.ssh.ssh_exe_cmd(cmd_rm)
        
    # start rsync
    def __start_rsync(self, cmd, src, dst, times, need_merged=False):
        output_dir_path = os.path.join(
            self.output_path, str(self.transfer_id))
        output_file_path = os.path.join(
            output_dir_path, f'{os.path.basename(src)}.out')
        
        with open(output_file_path, 'a', encoding='utf-8') as file_stream:
            # The first line is information about the receiver and the parent path of the file (folder)
            file_stream.write(f'{self.address} {os.path.dirname(src)}\n')
        popen = Popen(cmd, stdout=open(output_file_path, 'a', encoding='utf-8'),
                      stderr=PIPE, universal_newlines=True, shell=True)

        # pylint: disable=W0612
        _, stderr = popen.communicate()
        # try 3 times if failed
        if times < 3:
            if popen.returncode == 255:
                self.__start_rsync(cmd, src, dst, times+1, need_merged)
        else:
            if stderr:
                sys.stderr.write(stderr)
        os.remove(output_file_path)

        # for sub files splited
        if need_merged:
            end = False
            dir_temp_path = os.path.split(src)[0]
            self.split_lock.acquire()
            try:
                self.split_dict[dir_temp_path]['current'] += 1
                if self.split_dict[dir_temp_path]['current'] == self.split_dict[dir_temp_path]['count']:
                    end = True
            finally:
                self.split_lock.release()
                
            if end:
                # construct the common prefix of sub files
                dst_dir_path, dst_file_name = os.path.split(dst)
                last_underscore_index = dst_file_name.rfind('_')
                assert last_underscore_index != -1
                large_file_name = dst_file_name[:last_underscore_index]
                dst_temp_file_prefix = os.path.join(dst_dir_path, large_file_name)
                dst_file_full_path = os.path.join(os.path.split(dst_dir_path)[0], large_file_name)

                self.__merge_files(dst_temp_file_prefix, dst_file_full_path)
                self.split_dict.pop(dir_temp_path)
                # delete the sub files and temp dir locally
                shutil.rmtree(dir_temp_path)
        

    # transfer single file
    def __transfer_file(self, sub_path, need_merged=False): # sub_path为相对路径
        print(f'transfering file: {sub_path}')
        cmd = None

        src = os.path.join(os.path.split(self.src_path)[0], sub_path)
        dst = os.path.join(self.dst_path, sub_path)
        if self.__is_compressed(sub_path):
            cmd = f'rsync -a --progress -e \'ssh -p {self.port} -i {self.sshkey_path} -o \'LogLevel=QUIET\'\' \
                    {src} {self.user}@{self.address}:{dst} \
                    --partial --inplace'
        else:
            cmd = f'rsync -az --progress -e \'ssh -p {self.port} -i {self.sshkey_path} -o \'LogLevel=QUIET\'\' \
                    {src} {self.user}@{self.address}:{dst} \
                    --partial --inplace'
        self.__start_rsync(cmd, src, dst, 0, need_merged)
        return

    # transfer directory serial
    def __transfer_dir(self, sub_path):
        print(f'transfering dir: {sub_path}')
        src = os.path.join(os.path.split(self.src_path)[0], sub_path)
        dst = os.path.join(self.dst_path, os.path.split(sub_path)[0])
        cmd = f'rsync -az --progress  -e \'ssh -p {self.port} -i {self.sshkey_path} -o \'LogLevel=QUIET\'\' \
                {src} {self.user}@{self.address}:{dst} \
                --partial --inplace'

        self.__start_rsync(cmd, src, dst, 0)
        return

    def transfer_files(self):
        '''
        run to transfer files
        '''
        thread_num = config.THREADS
        self.thread_pool = ThreadPoolExecutor(
            thread_num, thread_name_prefix='scow-sync')
        
        self.file_queue.add_all_to_queue(
            self.src_path, self.max_depth)
        
        while not self.file_queue.empty():
            entity_file: files_queue.EntityFile = self.file_queue.get()
            if entity_file.is_dir:
                if entity_file.depth < self.max_depth: # mkdir for parallel transfer dir
                    cmd_mkdir = f'mkdir -p \
                                 {os.path.join(self.dst_path, entity_file.sub_path)}'
                    self.ssh.ssh_exe_cmd(cmd=cmd_mkdir)
                else:                                   # serial transfer dir
                    self.thread_pool.submit(
                        self.__transfer_dir, entity_file.sub_path)

            else:
                file_full_path = os.path.join(os.path.split(self.src_path)[0], entity_file.sub_path)
                file_size = os.path.getsize(file_full_path)
                if file_size >= config.SPLIT_THRESHOLD and entity_file.depth <= self.max_depth:
                    # split the large file
                    temp_dir_path = self.__split_large_file(file_full_path)
                    
                    cmd_mkdir_split_temp = f'mkdir -p \
                                 {os.path.join(os.path.split(os.path.join(self.dst_path, entity_file.sub_path))[0], os.path.basename(temp_dir_path))}'
                    self.ssh.ssh_exe_cmd(cmd=cmd_mkdir_split_temp)

                    for file in os.listdir(temp_dir_path):
                        self.thread_pool.submit(
                            self.__transfer_file, os.path.join(os.path.join(os.path.split(entity_file.sub_path)[0], os.path.split(temp_dir_path)[1]), file), True)
                else:
                    self.thread_pool.submit(
                        self.__transfer_file, entity_file.sub_path)
        self.thread_pool.shutdown()
        
        # delete the output dir
        os.rmdir(os.path.join(self.output_path, str(self.transfer_id)))
        sys.exit()
