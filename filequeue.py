import queue
import os
class FileQueue:

    class EntityFile:
        def __init__(self, filename, isdir, fatherpath):
            self.filename = filename
            self.isdir = isdir
            self.fatherpath = fatherpath


    def __init__(self):
        self.file_queue = queue.Queue(maxsize=0) # maxsize=0则队列大小无限制

    def __add_file_to_queue(self, sourcepath, fatherpath, filename):
        if os.path.isfile(sourcepath):
            self.file_queue.put(self.EntityFile(filename, False, fatherpath))
        else:
            self.file_queue.put(self.EntityFile(filename, True, fatherpath))
            for file in os.path.listdir(sourcepath):
                self.add_to_queue(os.path.join(sourcepath, file), os.path.join(fatherpath, filename), file)

    def add_to_queue(self, sourcepath) -> int:
        self.__add_file_to_queue(sourcepath, "", os.path.basename(sourcepath))
        return self.file_queue.qsize()