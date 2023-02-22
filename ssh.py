import paramiko
import threading

# 使用单例模式
class SSH:
    
    _instance_lock = threading.Lock()

    def __init__(self, address, user, password):
        self.ssh = paramiko.SSHClient()
        self.address = address
        self.user = user
        self.password = password
        self.__login(address, user, password)

    def __new__(cls, *args, **kwargs):
        if not hasattr(SSH, "_instance"):
            with SSH._instance_lock:
                if not hasattr(SSH, "_instance"):
                    SSH._instance = object.__new__(cls)  
        return SSH._instance
    
    def __login(self, address, user, password):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(address, username=user, password=password)
        return 
    
    def ssh_exe_cmd(self, cmd):
        [stdin, stdout, stderr] = self.ssh.exec_command(cmd)
        string_error = stderr.read().decode('utf-8')
        if string_error:
            raise Exception(string_error)
        return 
    