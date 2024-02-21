import paramiko
import sys

class RemoteCommand:
    def __init__ (self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect (self):
        print ("Connecting to %s@%s" % (self.username, self.hostname))

        try:
            self.client.connect(self.hostname, username=self.username, password=self.password)
            print("Successfully connected to %s" % self.hostname)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")

    def execute (self, command):
        stdin, stdout, stderr = self.client.exec_command(command)

        print("Command executed:")
        print(stdout.read().decode('utf-8'))

        error_output = stderr.read().decode('utf-8')
        if error_output:
            print("Error: %s" % error_output)

    def close (self):
        self.client.close()
        print("Connection to %s closed" % self.hostname)