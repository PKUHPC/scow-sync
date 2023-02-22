import paramiko

class SSH:
    
    def __init__(self):
        self.ssh = paramiko.SSHClient()

    def login(self, address, user, password):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(address, username=user, password=password)

    def ssh_exe_cmd(self,cmd):
        [stdin, stdout, stderr] = self.ssh.exec_command(cmd)
        string_error = stderr.read().decode('utf-8')
        if string_error:
            raise Exception(string_error)
        return 
    
    