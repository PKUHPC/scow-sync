import queue

import os

class EntityFile:
    def __init__(self, isdir, subpath):
        self.isdir = isdir
        self.subpath = subpath

class FileQueue:

    def __init__(self):
        self.file_queue = queue.Queue(maxsize=0)  # maxsize=0则队列大小无限制

    def __add_file_to_queue(self, sourcepath, subpath):
        if os.path.isfile(sourcepath):
            self.file_queue.put(EntityFile(False, subpath))
        else:
            self.file_queue.put(EntityFile(True, subpath))
            for file in os.listdir(sourcepath):
                self.__add_file_to_queue(
                    os.path.join(sourcepath, file),
                    os.path.join(subpath, file)
                )

    def empty(self):
        return self.file_queue.empty()

    def get(self):
        return self.file_queue.get()

    def add_to_queue(self, sourcepath) -> int:
        self.__add_file_to_queue(sourcepath, os.path.basename(sourcepath))
        return self.file_queue.qsize()
