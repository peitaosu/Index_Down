import os, sys, json
from shutil import copyfile
import urllib
from utils import *

def download(remote, local):
    if remote.startswith(r"\\"):
        # smb
        copyfile(remote, local)
    elif remote.startswith("http"):
        # http, https
        urllib.urlretrieve (remote, local)
    else:
        # unknown
        copyfile(remote, local)

def duplicate(local, dup):
    create_symlink(local, dup)

def download_from_index(remote, local, index_path):
    with open(index_path) as index_file:
        index = json.load(index_file)
    for file_hash in index.keys():
        remote_file = os.path.join(remote, index[file_hash][0])
        local_file = os.path.join(local, index[file_hash][0])
        download(remote_file, local_file)
        if len(index[file_hash]) > 1:
            for dup in index[file_hash][1:]:
                dup_file = os.path.join(local, dup)
                duplicate(local_file, dup_file)

if __name__ == "__main__":
    local_path = "."
    index_path = "down.index"
    if len(sys.argv) == 1:
        print("> python downloader.py <remote_path> [<local_path> [<index_path>]]")
        print("Please provide remote location.")
        sys.exit(-1)
    if len(sys.argv) > 1:
        remote_path = sys.argv[1]
    if len(sys.argv) > 2:
        local_path = sys.argv[2]
    if len(sys.argv) > 3:
        index_path = sys.argv[3]
    download_from_index(remote_path, local_path, index_path)