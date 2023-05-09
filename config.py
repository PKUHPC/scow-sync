'''
Config for scow-sync
'''
import os

SHEBANG_PATH = '/usr/bin/python3'
THREADS = 3
SCOWSYNC_PATH = os.path.expanduser('~/scow/.scow-sync')
LOG_PATH = os.path.join(SCOWSYNC_PATH, 'scow-sync.log')
ERROR_PATH = os.path.join(SCOWSYNC_PATH, 'scow-sync.err')
