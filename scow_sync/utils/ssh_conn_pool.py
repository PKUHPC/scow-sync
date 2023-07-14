import subprocess
import os
import fcntl

class SshConnectionPool:
    def __init__(self, address, port, username, conn_path, conn_count):
        self.address = address
        self.port = port
        self.username = username
        self.conn_path = conn_path
        self.conn_count = conn_count
        self.conns = []
        
    def initialize_pool(self):
        for i in range(self.conn_count):
            conn_file = f"{self.conn_path}/ssh_conn_{i}"
            command = f"ssh -M -S {conn_file} -fnNT {self.username}@{self.address} -p {self.port}"
            process = subprocess.Popen(command, shell=True)
            process.communicate()
            self.conns.append(conn_file)
        print("SSH Connection pool initialized.")
        
    def get_conn(self):
        for conn in self.conns:
            with open(conn, 'w') as f:
                try:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return conn
                except IOError:
                    continue
        raise Exception("No available connection in the pool.")
        
    def destroy_pool(self):
        for conn in self.conns:
            command = f"ssh -S {conn} -O exit {self.username}@{self.address}"
            process = subprocess.Popen(command, shell=True)
            process.communicate()
        print("SSH Connection pool destroyed.")
