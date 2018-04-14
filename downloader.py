import os, sys, json
from utils import *

def download(remote, local):
    pass

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
