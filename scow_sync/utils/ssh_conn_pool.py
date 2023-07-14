from subprocess import Popen
import os
import sys
import threading

class SshConnectionPool:
    def __init__(self, address, port, username, sshkey_path, conn_path, conn_count):
        self.address = address
        self.port = port
        self.username = username
        self.conn_path = conn_path
        self.conn_count = conn_count
        self.sshkey_path = sshkey_path
        self.conns = {}
        self.lock = threading.Lock()
        if not os.path.exists(conn_path):
            os.makedirs(self.conn_path)
        
    def __log(self, cmd, stdout, stderr):
        if stdout != '':
            sys.stdout.write(f"ssh execute command:{cmd}, stdout:{stdout}")
            sys.stdout.flush()
        if stderr != '':
            sys.stderr.write(f"ssh execute error:{cmd}, stderr:{stderr}")
            sys.stderr.flush()
        return stdout, stderr

    def initialize_pool(self):
        for i in range(self.conn_count):
            conn_file = f"{self.conn_path}/ssh_conn_{i}"
            command = f"ssh -M -S {conn_file} -fnNT {self.username}@{self.address} -p {self.port} -i {self.sshkey_path} | exit"
            process = Popen(command, shell=True)
            process.communicate()
            self.conns[conn_file] = False
        print("SSH Connection pool initialized.")
        
    def get_conn(self):
        with self.lock:
            for conn, in_use in self.conns.items():
                if not in_use:
                    self.conns[conn] = True
                    return conn
            raise Exception("Error: No available connection in the pool.")
        
    def release_conn(self, conn):
        with self.lock:
            if conn in self.conns and self.conns[conn]:
                self.conns[conn] = False  # Mark the connection as not in use.
            else:
                raise Exception("Trying to release an invalid or unused connection.")
        
        
    def destroy_pool(self):
        for conn in self.conns:
            command = f"ssh -S {conn} -O exit {self.username}@{self.address}"
            process = Popen(command, shell=True)
            process.communicate()
            
        os.rmdir(self.conn_path)
        print("SSH Connection pool destroyed.")



# if __name__ == '__main__':
#     ssh = SshConnectionPool(address="pku", port=22, username="root", sshkey_path="/home/ljz/.ssh/id_rsa", conn_path="/home/ljz/scow/.scow-sync", conn_count=3)
#     ssh.initialize_pool()

#     ssh_session1 = ssh.get_conn()
#     cmd1 = f"rsync -az --progress -e 'ssh -S ${ssh_session1}' /home/ljz/scow-sync/tests/parallel/send_files/file1 root@pku:/root/file-transfer/file-test --partial --inplace"
#     process1 = Popen(cmd1, shell=True)
#     process1.communicate()
#     ssh.release_conn(ssh_session1)
#     ssh_session2 = ssh.get_conn()
#     cmd2 = f"rsync -az --progress -e 'ssh -S ${ssh_session2}' /home/ljz/scow-sync/tests/parallel/send_files/file2 root@pku:/root/file-transfer/file-test --partial --inplace"
#     process2 = Popen(cmd2, shell=True)
#     process2.communicate()
#     ssh.release_conn(ssh_session2)
