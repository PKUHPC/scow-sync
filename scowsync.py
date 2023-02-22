import os
import queue
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from filequeue import FileQueue
from ssh import SSH

class ScowSync:

    def __init__(self, address, user, sshpassword, sourcepath, destinationpath):
        self.address = address
        self.user = user
        self.sshpassword = sshpassword
        self.sourcepath = sourcepath
        self.destinationpath = destinationpath
        
        self.compress_list = ['.tar', '.zip', '.rar', '.7z', '.gz', '.bz2', '.xz', '.tgz', 'tbz', 'tb2', 'taz', 'tlz', 'txz']
        self.file_queue = FileQueue()

    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False
    
    # transfer single file
    def __transfer_file(self, filepath):
        print('transfering file: {}'.format(filepath))
        if(self.__is_compressed(filepath)):
            cmd = 'sshpass -p {} rsync -a {} {}@{}:{} --partial --inplace'.format(self.sshpassword, filepath, self.user, self.address, os.path.join(self.destinationpath, filepath))
            result = os.system(cmd)
            if result != 0:
                raise Exception('transfer {} failed'.format(filepath))
        else:
            cmd = 'sshpass -p {} rsync -az {} {}@{}:{} --partial --inplace'.format(self.sshpassword, filepath, self.user, self.address, os.path.join(self.destinationpath, filepath))
            result = os.system(cmd)
            if result != 0:
                raise Exception('transfer {} failed'.format(filepath))
            
    # run trnsferring files with mutithreads
    def transfer_files(self):
        thread_num = min(self.file_queue.add_to_queue(self.sourcepath), 2*cpu_count()+1)
        self.thread_pool = ThreadPoolExecutor(thread_num, thread_name_prefix='scowsync')
        while(not self.file_queue.empty()):
            entity_file = self.file_queue.get()
            if entity_file.isdir:
                ssh = SSH(self.address, self.user, self.sshpassword)
                string_cmd = 'mkdir -p {}'.format(os.path.join(self.destinationpath, os.path.join(entity_file.fatherpath, entity_file.filename)))
                print("ssh command: {}".format(string_cmd))
                ssh.ssh_exe_cmd(cmd=string_cmd)
            else:
                self.thread_pool.submit(self.__transfer_file, os.path.join(entity_file.fatherpath, entity_file.filename))
        self.thread_pool.shutdown()