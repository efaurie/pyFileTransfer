import os

from FTPHandler import FTPHandler


class FileTransferHandler:
    def __init__(self, destination, username=None, password=None):
        self.destination = destination
        if not os.path.exists(destination):
            os.makedirs(destination)

        if not self.is_local:
            self.ftp_handler = FTPHandler(self.hostname, username, password)
            self.ftp_handler.remote_cd(self.destination_directory)

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

    @property
    def is_local(self):
        if '@' in self.destination:
            return False
        else:
            return True

    @property
    def hostname(self):
        return self.destination.split('@')[0]

    @property
    def destination_directory(self):
        return self.destination.split('@')[1]

    # Attempt to rename file
    # If it can, file isn't being written to by another process
    def file_is_ready(self, source_file):
        try:
            os.rename(source_file, '{0}.tmp'.format(source_file))
            os.rename('{0}.tmp'.format(source_file), source_file)
            return True
        except:
            return False

    def local_transfer(self, source_file):
        filename = os.path.basename(source_file)
        os.rename(source_file, '{0}/{1}'.format(self.destination, filename))

    def remote_transfer(self, source_file):
        self.ftp_handler.transfer_file(source_file)

    @staticmethod
    def remove_file(source_file):
        os.remove(source_file)
