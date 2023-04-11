'''
Ssh connection and execute commands with singleton pattern
'''
import threading
import paramiko

class SSH:
    '''
    Ssh connection and execute commands
    '''
    _instance_lock = threading.Lock()

    def __init__(self, address, user, sshkey_path, port):
        self.ssh = paramiko.SSHClient()
        self.address = address
        self.user = user
        self.port = port
        self.__login(address, user, sshkey_path, port)
    
    # pylint: disable=W0613
    def __new__(cls, *args, **kwargs):
        if not hasattr(SSH, "_instance"):
            with SSH._instance_lock:
                if not hasattr(SSH, "_instance"):
                    SSH._instance = object.__new__(cls)
        return SSH._instance

    def __login(self, address, user, sshkey_path, port):
        key = paramiko.RSAKey.from_private_key_file(sshkey_path)
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(address, username=user, pkey=key, port=port)

    def ssh_exe_cmd(self, cmd):
        '''
        Execute command on the server
        '''
        try:
            self.ssh.exec_command(cmd)
        except SystemError as exception:
            print(f"ssh execute error:{cmd}, exception:{str(exception)}")
               
    def ssh_rm_file(self, filepath):
        '''
        delete the file on remote server and don't catch error when the file is not exist
        '''
        try:
            self.ssh.exec_command(f'rm -rf {filepath}')
        except SystemError as exception:
            print(f'ssh execute error: rm -rf {filepath}, exception:{str(exception)}')
