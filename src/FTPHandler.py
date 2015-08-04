import os
import paramiko


class FTPHandler:
    def __init__(self, hostname, destination_directory, username=None, password=None):
        self.sftp = None
        self.sftp_connection = paramiko.Transport((hostname, 22))
        self.destination_directory = destination_directory
        self.connect(username, password)

    def connect(self, username, password):
        if username is None:
            self.sftp_connection.connect()
        else:
            self.sftp_connection.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.sftp_connection)

    def transfer_file(self, source_file_path):
        self.sftp.put(source_file_path, '{0}{1}'.format(self.destination_directory, os.path.basename(source_file_path)))

    def disconnect(self):
        self.sftp.close()
        self.sftp_connection.close()
