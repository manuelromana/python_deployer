import paramiko
import config
import socket
import subprocess


class Ssh_utils:
    "Class to ssh the remote"

    def __init__(self):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host = config.HOST
        self.username = config.USERNAME
        self.password = config.PASSWORD
        self.timeout = float(config.TIMEOUT)
        self.commands = config.COMMANDS

    def connect(self):
        "Login to the remote server"
        try:
            # Paramiko.SSHClient can be used to make connections to the remote
            # server and transfer files
            print("Establishing ssh connection...")
            self.client = paramiko.SSHClient()
            # Parsing an instance of the AutoAddPolicy to
            #  changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Connect to the server
            if (self.password == ''):
                private_key = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(hostname=self.host, port=self.port,
                                    username=self.username,
                                    pkey=private_key, timeout=self.timeout,
                                    allow_agent=False, look_for_keys=False)
                print("Connected to the server", self.host)
            else:
                self.client.connect(hostname=self.host,
                                    username=self.username,
                                    password=self.password,
                                    timeout=self.timeout,
                                    allow_agent=False, look_for_keys=False)
                print("Connected to the server", self.host)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print("Connection timed out")
            result_flag = False
        except Exception as e:
            print('\nException in connecting to the server')
            print('PYTHON SAYS:', e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        return result_flag

    def execute_command(self, commands):
        """Execute a command on the remote host
        return stdout stderr from bash and stdin
        """
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                print("checking if docker installed ...")
                print("Executing command --> dpkg -l docker-ce| grep docker ")
                # Do not depend on the exit code of dpkg -l packagename,
                #  as it might return with a 0 exit code
                # even if the package is not fully installed
                #  github.com/bitrise-io/bitrise/issues/433 – Viktor Benei
                stdin, stdout, stderr = self.client.exec_command(
                    "dpkg -l docker-ce |grep docker", timeout=10)
                self.ssh_output = stdout.read()
                self.ssh_error = stderr.read()
                if self.ssh_error:
                    print(self.ssh_error)
                    print("No package docker")
                    print("got to install it...")
                    for command in commands:
                        print("Executing command --> {}".format(command))
                        stdin, stdout, stderr = self.client.exec_command(
                            command)
                        self.ssh_output = stdout.read()
                        self.ssh_error = stderr.read()
                        if self.ssh_error:
                            print("Problem occurred while running command:",
                                  command, " The error is ", self.ssh_error)
                            result_flag = False
                        else:
                            print("bash: ", self.ssh_output, "\n"
                                  "Command execution completed successfully",
                                  command)
                else:
                    print(str(self.ssh_output, 'utf-8'))
                    print("docker-ce is intalled :) !")
                    print("checking version...")
                    print("Executing command-->dpkg -l docker-ce|grep 19.03")
                    stdin, stdout, stderr = self.client.exec_command(
                        "dpkg -l docker-ce |grep 19.03", timeout=10)
                    self.ssh_output = stdout.read()
                    self.ssh_error = stderr.read()
                    print(self.ssh_output == "")
                    if self.ssh_output == "":
                        print("docker is not up-to-date")
                    else:
                        print(str(self.ssh_output, 'utf-8'))
                        print("version up to date :)")

            else:
                print("Could not establish SSH connection")
                result_flag = False
        except socket.timeout as e:
            print("Command timed out.", command)
            self.client.close()
            result_flag = False
        except paramiko.SSHException:
            print("Failed to execute the command!", command)
            self.client.close()
            result_flag = False

        return result_flag

    def build_service(self, folder_name, list_files):
        "This method uploads the file to remote server"
        result_flag = True
        try:
            if self.connect():
                ftp_client = self.client.open_sftp()

                print("getting local path with pwd")
                cmd = subprocess.run(
                    ["pwd"], capture_output=True)
                pwd = str(cmd.stdout, "utf-8")
                if cmd.stderr is True:
                    print(cmd.stderr)
                else:
                    print("Working dir is {}".format(pwd[:-1]))

                print(("creating {} folder in remote...").format(folder_name))

                stdin, stdout, stderr = self.client.exec_command(
                    "cd && mkdir {}".format(folder_name), timeout=10)
                self.ssh_output = stdout.read()
                self.ssh_error = stderr.read()

                for file_path in list_files:
                    print("sftp coping {} in remote {}".format(
                        file_path, folder_name))
                    ftp_client.put(pwd[:-1]+file_path,
                                   "/root"+file_path)
                for command in config.COMMANDS_BUILD_CHECKER:
                    print("Executing command --> {}".format(command))
                    stdin, stdout, stderr = self.client.exec_command(
                        command)
                    self.ssh_output = stdout.read()
                    self.ssh_error = stderr.read()
                    if self.ssh_error:
                        print("Problem occurred while running command:",
                              command, " The error is ", self.ssh_error)
                        result_flag = False
                    else:
                        print("bash: ", self.ssh_output, "\n"
                              "Command execution completed successfully",
                              command)

                ftp_client.close()
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False
        except Exception as e:
            print('\nUnable to upload the file to the remote server')
            print('PYTHON SAYS:', e)
            result_flag = False
            ftp_client.close()
            self.client.close()

        return result_flag
