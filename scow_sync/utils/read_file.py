import os


def read_tail(file_path, n):
    """读取文件的最后 n 行"""
    with open(file_path, 'rb') as f:
        # 设置偏移量到文件末尾
        f.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer_location = f.tell()
        line_count = 0

        # 从文件末尾开始读取，直到读取到所需的行数
        while pointer_location >= 0 and line_count < n:
            f.seek(pointer_location)
            byte = f.read(1)
            if byte == b'\n':
                line_count += 1
            buffer.extend(byte)
            pointer_location -= 1
        
        # 最后的数据可能没有换行符，需要补上
        if buffer and buffer[-1] != b'\n':
            buffer.append(b'\n')

        return buffer.decode('utf-8')[::-1]  # 返回解码后的数据，顺序反转

def read_head(file_path, n):
    """读取文件的前 n 行"""
    with open(file_path, 'r') as f:
        return ''.join([f.readline() for _ in range(n)])
