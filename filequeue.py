'''
Add files to queue and get files from queue
'''
import queue
import os


class EntityFile:
    '''
    Element of file queue
    '''

    def __init__(self, isdir, subpath, depth):
        self.isdir = isdir
        self.subpath = subpath
        self.depth = depth


class FileQueue:
    '''
    Queue of files
    '''

    def __init__(self):
        self.file_queue = queue.Queue(maxsize=0)  # maxsize=0则队列大小无限制

    def __add_file_to_queue(self, sourcepath, subpath, depth, maxdepth):
        if os.path.isfile(sourcepath):
            self.file_queue.put(EntityFile(False, subpath, depth))
        else:
            if depth <= maxdepth:
                self.file_queue.put(EntityFile(True, subpath, depth))
                for file in os.listdir(sourcepath):
                    self.__add_file_to_queue(
                        os.path.join(sourcepath, file),
                        os.path.join(subpath, file),
                        depth+1,
                        maxdepth
                    )
            else:
                self.file_queue.put(EntityFile(True, subpath, depth))

    def empty(self):
        '''
        Return True if queue is empty
        '''
        return self.file_queue.empty()

    def get(self):
        '''
        Get file from queue
        '''
        return self.file_queue.get()

    def add_all_to_queue(self, sourcepath, max_depth) -> int:
        '''
        Add files to queue in recursive form
        @param sourcepath: source path
        @param max_depth: max depth of recursion
        @return: size of queue
        '''
        self.__add_file_to_queue(
            sourcepath, os.path.basename(sourcepath), 0, max_depth)
        return self.file_queue.qsize()
