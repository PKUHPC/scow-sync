'''
全局工具函数
'''
import hashlib
import time


def gen_file_transfer_id(cmd: str):
    '''
    生成唯一的transferid
    '''
    hash_object = hashlib.md5(cmd.encode())
    hash_value = int.from_bytes(hash_object.digest(), byteorder='big')
    modulus = 10**9 + 7
    unique_id = hash_value % modulus
    return unique_id


class Timer:
    '''
    计时器
    with Timer():
        ....
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
