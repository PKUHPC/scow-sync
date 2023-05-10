'''
Config for scow-sync
'''
import os

THREADS = 3
SHEBANG_PATH = '/usr/bin/python3'
SCOWSYNC_PATH = os.path.expanduser('~/scow/.scow-sync')
LOG_PATH = os.path.join(SCOWSYNC_PATH, 'scow-sync.log')
ERROR_PATH = os.path.join(SCOWSYNC_PATH, 'scow-sync.err')
