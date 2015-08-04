import os

from ftplib import FTP


class FTPHandler:
    def __init__(self, hostname, username=None, password=None):
        self.ftp_connection = FTP(hostname)
        self.connect(username, password)

    def connect(self, username, password):
        if username is None:
            self.ftp_connection.login()
        else:
            self.ftp_connection.login(username, password)

    def remote_cd(self, destination_directory):
        self.ftp_connection.cwd(destination_directory)

    def transfer_file(self, source_file_path):
        source_file = open(source_file_path, 'rb')

        source_filename = os.path.basename(source_file_path)
        put_command = 'STOR {0}'.format(source_filename)

        self.ftp_connection.storbinary(put_command, source_file)

    def disconnect(self):
        self.ftp_connection.quit()
