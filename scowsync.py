'''
Transfer files from local to remote server on SCOW
'''
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor
from subprocess import Popen, PIPE
import utils
from filequeue import FileQueue, EntityFile
from ssh import SSH
from config import SCOWSYNC_PATH, THREADS, SPLIT_THRESHOLD, SPLIT_CHUNK_SIZE


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
        self.split_dict = {}
        self.thread_pool = None
        self.raw_string = f'{address} {user} {sourcepath} {destinationpath}'

        self.transfer_id = utils.gen_file_transfer_id(self.raw_string)
        self.base_path = SCOWSYNC_PATH

    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False

    # split large file
    def __split_large_file(self, filepath) -> str:
        '''
        切分filepath大文件，返回存储切分后的大文件的目录路径
        '''
        print(f'spliting large file: {filepath}')
        dir_path = f'{filepath}_sstemp'
        os.makedirs(dir_path, 0o700)
        file_name = os.path.basename(filepath)
        cmd = f'split -b {SPLIT_CHUNK_SIZE}M {filepath} {dir_path}/{file_name}_'
        popen = Popen(cmd, stderr=PIPE, universal_newlines=True, shell=True)
        _, stderr = popen.communicate()
        if stderr:
            sys.stderr.write(stderr)
            return None  # type: ignore
        # 统计下划分的文件数量
        count = 0
        file_list = os.listdir(dir_path)
        count = len(file_list)
        split_element = {'count': count, 'current': 0}
        self.split_dict.update({dir_path: split_element})
        return dir_path

    # merge files
    def __merge_files(self, dst_temp_file_prefix, dst_file_path):
        
        cmd_cat = f'cat {dst_temp_file_prefix}_* > {dst_file_path}'
        print("cmd_cat", cmd_cat)
        ssh = SSH(self.address, self.user,
                              self.sshkey_path, self.port)
        ssh.ssh_exe_cmd(cmd_cat)
        
        dst_temp_dir_path: str = os.path.split(dst_temp_file_prefix)[0]
        cmd_rm = f'rm -rf {dst_temp_dir_path}'
        ssh.ssh_exe_cmd(cmd_rm)
        
    # start rsync
    def __start_rsync(self, cmd, src, dst, times, need_merge=False):
        output_dir_path = os.path.join(
            self.base_path, str(self.transfer_id))
        output_file_path = os.path.join(
            output_dir_path, f'{os.path.basename(src)}.out')
        with open(output_file_path, 'a', encoding='utf-8') as file_stream:
            # 第一行是关于接收集群和文件（文件夹）的父路径的信息
            file_stream.write(f'{self.address} {os.path.dirname(src)}\n')
        popen = Popen(cmd, stdout=open(output_file_path, 'a', encoding='utf-8'),
                      stderr=PIPE, universal_newlines=True, shell=True)

        # 等待进程结束
        # pylint: disable=W0612
        _, stderr = popen.communicate()
        if times < 3:
            if popen.returncode == 255:
                self.__start_rsync(cmd, src, dst, times+1, need_merge)
        else:
            if stderr:
                sys.stderr.write(stderr)
        os.remove(output_file_path)
        # 对于需要merge的files splitted
        if need_merge:
            dir_temp_path = os.path.split(src)[0]
            self.split_dict[dir_temp_path]['current'] += 1
            if self.split_dict[dir_temp_path]['current'] == self.split_dict[dir_temp_path]['count']:
                # 文件前缀
                dst_dir_path, dst_file_name = os.path.split(dst)
                last_underscore_index = dst_file_name.rfind('_')
                assert last_underscore_index != -1
                large_file_name = dst_file_name[:last_underscore_index]
                dst_temp_file_prefix = os.path.join(dst_dir_path, large_file_name)
                dst_file_path = os.path.join(os.path.split(dst_dir_path)[0], large_file_name)
                self.__merge_files(dst_temp_file_prefix, dst_file_path)
                self.split_dict.pop(dir_temp_path)
                # 删除本地的
                shutil.rmtree(dir_temp_path)
        

    # transfer single file
    def __transfer_file(self, filepath, need_merge=False):
        print(f'transfering file: {filepath}')
        cmd = None
        # [0] is direcctory [1] is filename
        src = os.path.join(os.path.split(self.sourcepath)[0], filepath)
        dst = os.path.join(self.destinationpath, filepath)
        if self.__is_compressed(filepath):
            cmd = f'rsync -a --progress -e \'ssh -p {self.port} -i {self.sshkey_path} -o \'LogLevel=QUIET\'\' \
                    {src} {self.user}@{self.address}:{dst} \
                    --partial --inplace'
        else:
            cmd = f'rsync -az --progress -e \'ssh -p {self.port} -i {self.sshkey_path} -o \'LogLevel=QUIET\'\' \
                    {src} {self.user}@{self.address}:{dst} \
                    --partial --inplace'
        self.__start_rsync(cmd, src, dst, 0, need_merge)
        return

    # transfer directory
    def __transfer_dir(self, dirpath):
        print(f'transfering dir: {dirpath}')
        src = os.path.join(os.path.split(self.sourcepath)[0], dirpath)
        dst = os.path.join(self.destinationpath, os.path.split(dirpath)[0])
        cmd = f'rsync -az --progress  -e \'ssh -p {self.port} -i {self.sshkey_path} -o \'LogLevel=QUIET\'\' \
                {src} {self.user}@{self.address}:{dst} \
                --partial --inplace'

        self.__start_rsync(cmd, src, dst, 0)
        return

    def transfer_files(self):
        '''
        run to transfer files
        '''
        thread_num = THREADS
        self.thread_pool = ThreadPoolExecutor(
            thread_num, thread_name_prefix='scow-sync')
        self.file_queue.add_all_to_queue(
            self.sourcepath, self.max_depth)
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
                file_path = os.path.join(os.path.split(
                    self.sourcepath)[0], entity_file.subpath)
                file_size = os.path.getsize(file_path)
                if file_size >= SPLIT_THRESHOLD and entity_file.depth < self.max_depth:
                    # 需要切分
                    temp_dir_path = self.__split_large_file(file_path)
                    ssh = SSH(self.address, self.user,
                              self.sshkey_path, self.port)
                    string_cmd = f'mkdir -p \
                                 {os.path.join(self.destinationpath, os.path.basename(temp_dir_path))}'
                    ssh.ssh_exe_cmd(cmd=string_cmd)
                    for file in os.listdir(temp_dir_path):
                        self.thread_pool.submit(
                            self.__transfer_file, os.path.join(os.path.basename(temp_dir_path), file), True)
                else:
                    self.thread_pool.submit(
                        self.__transfer_file, entity_file.subpath)
        self.thread_pool.shutdown()
        os.rmdir(os.path.join(self.base_path, str(self.transfer_id)))
        sys.exit()
