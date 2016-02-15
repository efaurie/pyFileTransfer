import os
import time

from FTPHandler import FTPHandler


class FileTransferHandler:
    def __init__(self, destination, username=None, password=None, poll_time=30):
        self.destination = destination
        self.poll_time = poll_time
        if self.is_local and not os.path.exists(destination):
            os.makedirs(destination)

        if not self.is_local:
            self.ftp_handler = FTPHandler(self.hostname, self.destination_directory, username, password)

    @staticmethod
    def remove_file(source_file):
        os.remove(source_file)

    @property
    def is_local(self):
        if '@' in self.destination:
            return False
        else:
            return True

    @property
    def hostname(self):
        if self.is_local:
            return 'localhost'
        else:
            return self.destination.split('@')[0]

    @property
    def destination_directory(self):
        if self.is_local:
            destination_directory = self.destination
        else:
            destination_directory = self.destination.split('@')[1]

        if not destination_directory.endswith('/'):
            destination_directory += '/'

        return destination_directory

    def transfer(self, source_file):
        if not self.file_is_ready(source_file):
            print '[Skipping] Still Being Written: {0}'.format(os.path.basename(source_file))
            return

        print '[Transferring] {0}'.format(os.path.basename(source_file))
        if self.is_local:
            self.local_transfer(source_file)
        else:
            self.remote_transfer(source_file)
            print '[Removing] {0}'.format(os.path.basename(source_file))
            self.remove_file(source_file)

    def file_is_ready(self, source_file):
        initial_size = os.stat(source_file).st_size
        time.sleep(self.poll_time)
        post_size = os.stat(source_file).st_size
        if initial_size == post_size:
            return True
        else:
            return False

    def local_transfer(self, source_file):
        filename = os.path.basename(source_file)
        os.rename(source_file, '{0}{1}'.format(self.destination_directory, filename))

    def remote_transfer(self, source_file):
        self.ftp_handler.transfer_file(source_file)
