'''
Config for scow-sync
'''
import os

THREADS = 3
SHEBANG_PATH = '/usr/bin/python3'
OUTPUT_PATH = os.path.expanduser('~/scow/.scow-sync')
LOG_PATH = os.path.join(OUTPUT_PATH, 'scow-sync.log')
ERROR_PATH = os.path.join(OUTPUT_PATH, 'scow-sync.err')
SPLIT_THRESHOLD = 2 * 1024 * 1024 * 1024 # B
SPLIT_CHUNK_SIZE = 400 # MB
