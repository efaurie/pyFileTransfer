# pyFileTransfer

pyFileTransfer is a python application for automatically transferring local files to another location (remote via sftp, or local via copy).
It is designed to watch an assigned directory and transfer files as they become available.

# Usage
### Requirments
- Python 2.7
- Paramiko (SFTP Library)

### Arguments
- source
    - The source directory to watch
- destination
    - The destination directory
    - Local Format: /path/to/local/directory/
    - Remote Format: hostname@/path/to/remote/dir/
- username
    - The username for remote sftp login
- password
    - The password for remote sftp login
- spoll
    - The time to wait between checks of the source directory in seconds
    - Default: 300 (5 Minutes)
- fpoll
    - This solves a problem with files that are currently being written to the directory
    - Poll the file size twice, if the size hasn't changed, then it's fully written
    - fpoll is the time between file size polls in seconds
    - Default: 30

### Example
```sh
python pyFileTransfer.py -source /where/my/data/is/ -destination 192.168.1.1@/where/it/should/go/ -username foo -password bar
```