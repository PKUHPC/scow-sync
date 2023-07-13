'''
SSH functions
'''
import sys
import paramiko

class SSH:

    def __init__(self, address, user, sshkey_path, port):
        self.address = address
        self.user = user
        self.sshkey_path = sshkey_path
        self.port = port
        self.ssh = None

    def __login(self, address, user, sshkey_path, port):
        self.ssh = paramiko.SSHClient()
        key = paramiko.RSAKey.from_private_key_file(sshkey_path)
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(address, username=user, pkey=key, port=port)

    def __close(self):
        if self.ssh:
            self.ssh.close()

    def __log(self, cmd, stdout, stderr):
        stdout_str = stdout.read().decode()
        stderr_str = stderr.read().decode()
        if stdout_str != '':
            sys.stdout.write(f"ssh execute command:{cmd}, stdout:{stdout_str}")
            sys.stdout.flush()
        if stderr_str != '':
            sys.stderr.write(f"ssh execute error:{cmd}, stderr:{stderr_str}")
            sys.stderr.flush()
        return stdout_str, stderr_str

    def exec_cmd(self, cmd):
        '''
        execute command on the server
        @param cmd: the command to be executed
        @return stdout_str, stderr_str: the stdout and the stderr that have been parsed
        '''
        try:
            self.__login(self.address, self.user, self.sshkey_path, self.port)
            assert self.ssh
            _, stdout, stderr =  self.ssh.exec_command(cmd)
            return self.__log(cmd, stdout, stderr)
        finally:
            self.__close()

    def delete_file(self, file_path):
        '''
        delete the file 
        '''
        _, stderr = self.exec_cmd(f"rm -f {file_path}")
        if stderr != '':
            raise Exception(stderr)
        


    def delete_dir(self, dir_path):
        '''
        delete the directory
        '''
        _, stderr = self.exec_cmd(f"rm -rf {dir_path}")
        if stderr != '':
            raise Exception(stderr)
    
    def exist_file(self, file_path):
        '''
        check if the file exists on remote server
        '''
        _, stderr_str = self.exec_cmd(f"stat {file_path}")
        if stderr_str != '':
            return False
        return True