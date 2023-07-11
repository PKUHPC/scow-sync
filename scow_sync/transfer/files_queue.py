'''
Add files to queue and get files from queue
'''
import queue
import os


class EntityFile:
    '''
    Element of file queue
    '''
    def __init__(self, is_dir, sub_path, depth):
        self.is_dir = is_dir
        self.sub_path = sub_path
        self.depth = depth


class FileQueue:
    '''
    Queue of files
    '''

    def __init__(self):
        self.file_queue = queue.Queue(maxsize=0)  # unlimited queue size

    def __add_file_to_queue(self, full_path, sub_path, depth, max_depth):
        # father_path is the directory of source path from command line, then sub_path is the rest
        if os.path.isfile(full_path):
            self.file_queue.put(EntityFile(False, sub_path, depth))
        else:
            if depth < max_depth:
                self.file_queue.put(EntityFile(True, sub_path, depth))
                for file_name in os.listdir(full_path):
                    self.__add_file_to_queue(
                        os.path.join(full_path, file_name),
                        os.path.join(sub_path, file_name),
                        depth+1,
                        max_depth
                    )
            else:
                self.file_queue.put(EntityFile(True, sub_path, depth))

    def empty(self):
        '''
        return true if queue is empty
        '''
        return self.file_queue.empty()

    def get(self):
        '''
        get file from queue
        '''
        return self.file_queue.get()

    def add_all_to_queue(self, src_path, max_depth) -> int:
        '''
        add files to queue in recursive form
        @param sourcepath: source path
        @param max_depth: max depth of recursion
        @return: size of queue
        '''
        self.__add_file_to_queue(
            src_path, os.path.basename(src_path), 0, max_depth)
        return self.file_queue.qsize()
