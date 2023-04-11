'''
全局工具函数
'''
import hashlib


def gen_file_transfer_id(cmd: str):
    '''
    生成唯一的transferid
    '''
    hash_object = hashlib.md5(cmd.encode())
    hash_value = int.from_bytes(hash_object.digest(), byteorder='big')
    modulus = 10**9 + 7
    unique_id = hash_value % modulus
    return unique_id
