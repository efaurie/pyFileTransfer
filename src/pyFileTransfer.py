import time
import argparse

from os import listdir
from os.path import isfile, join
from FileTransferHandler import FileTransferHandler


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-source', help='The source directory to watch')
    parser.add_argument('-destination', help='The destination for files')
    parser.add_argument('-username', default=None, help='The FTP Username if remote')
    parser.add_argument('-password', default=None, help='The FTP Password if remote')
    parser.add_argument('-spoll', default=2, type=int, help='The polling time of source directory in seconds')
    parser.add_argument('-fpoll', default=30, type=int, help='The polling time of a file size to determine readiness in seconds')
    return parser.parse_args()


def watch_source(source_directory, file_handler, polling_time):
    try:
        while True:
            print '\nChecking Directory {0}'.format(source_directory)

            files_found = [join(source_directory, filename) for filename in listdir(source_directory) if isfile(join(source_directory, filename))]
            if len(files_found) > 0:
                print 'Found {0} Files In Directory!'.format(len(files_found))
                for file_path in files_found:
                    file_handler.transfer(file_path)
            else:
                print 'No New Files In Directory, Sleeping...'

            time.sleep(polling_time)
    except KeyboardInterrupt:
        print 'Stopping Transfer Daemon...'


if __name__ == '__main__':
    arguments = init()
    file_handler = FileTransferHandler(arguments.destination, arguments.username, arguments.password, arguments.fpoll)
    watch_source(arguments.source, file_handler, arguments.spoll)
