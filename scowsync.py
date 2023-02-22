import os
import queue
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

class ScowSync:

    def __init__(self, address, user, sshpassword, sourcepath, destinationpath):
        self.address = address
        self.user = user
        self.sshpassword = sshpassword
        self.sourcepath = sourcepath
        self.destinationpath = destinationpath
        
        self.compress_list = ['.tar', '.zip', '.rar', '.7z', '.gz', '.bz2', '.xz']
        self.file_queue = queue.Queue(maxsize=0) # maxsize=0则队列大小无限制
    
    # compress uncompressed files
    def __is_compressed(self, filename) -> bool:
        if '.' in filename:
            ext = filename.split('.')[-1]
            if ext in self.compress_list:
                return True
        return False
        

    # add files to queue and return the num of files
    def __add_to_queue(self, path):
        if os.path.isfile(path):
            self.file_queue.put(path)
        else:
            for file in os.listdir(path):
                self.__add_to_queue(os.path.join(path, file))
        return self.file_queue.qsize()
    
    # transfer single file
    def __transfer_file(self, filepath):
        print('transfering file: {}'.format(filepath))
        if(self.__is_compressed(filepath)):
            cmd = 'sshpass -p {} rsync -a {} {}@{}:{} --partial --inplace --progress'.format(self.sshpassword, filepath, self.user, self.address, self.destinationpath)
            result = os.system(cmd)
            if result != 0:
                raise Exception('transfer {} failed'.format(filepath))
        else:
            cmd = 'sshpass -p {} rsync -az {} {}@{}:{} --partial --inplace --progress'.format(self.sshpassword, filepath, self.user, self.address, self.destinationpath)
            result = os.system(cmd)
            if result != 0:
                raise Exception('transfer {} failed'.format(filepath))
            
    # run trnsferring files with mutithreads
    def transfer_files(self):
        thread_num = min(self.__add_to_queue(self.sourcepath), 2*cpu_count()+1)
        self.thread_pool = ThreadPoolExecutor(thread_num, thread_name_prefix='scowsync')
        while(not self.file_queue.empty()):
            self.thread_pool.submit(self.__transfer_file, self.file_queue.get())
        self.thread_pool.shutdown()