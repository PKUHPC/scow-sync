import time

class Timer:
    '''
    Compute the time of program by 'with Timer():'
    '''
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_time = (self.end_time - self.start_time) * 1000  # 转换为毫秒
        print(f"程序运行时间：{self.elapsed_time:.3f} ms")