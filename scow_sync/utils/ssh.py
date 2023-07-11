'''
SSH functions
'''
import paramiko

class SSH:

    def __init__(self, address, user, sshkey_path, port):
        self.ssh = paramiko.SSHClient()
        self.address = address
        self.user = user
        self.sshkey_path = sshkey_path
        self.port = port

    def __login(self, address, user, sshkey_path, port):
        key = paramiko.RSAKey.from_private_key_file(sshkey_path)
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(address, username=user, pkey=key, port=port)

    def ssh_exe_cmd(self, cmd):
        '''
        execute command on the server
        '''
        try:
            self.__login(self.address, self.user, self.sshkey_path, self.port)
            self.ssh.exec_command(cmd)
        except Exception as exception: # pylint: disable=broad-exception-caught
            print(f"ssh execute error:{cmd}, exception:{str(exception)}")
        finally:
            self.ssh.close()
                                                                                                                                                                                                         
    def ssh_rm_file(self, filepath):
        '''
        delete the file on remote server and don't throw error when the file is not exist
        '''
        try:
            self.ssh.exec_command(f'rm -rf {filepath}')
        except Exception as exception: # pylint: disable=broad-exception-caught
            print(f'ssh delete error: rm -rf {filepath}, exception:{str(exception)}')
