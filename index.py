import os, sys, json
from shutil import copyfile
import urllib
from utils import *

class Index():

    def __init__(self):
        self.dir_path = None
        self.index_file = None
        self.remote = None
        self.local = None
        self.UNI = {}
        self.DUP = {}
    
    def set_dir_path(self, dir_path):
        self.dir_path = dir_path
    
    def get_dir_path(self):
        return self.dir_path
    
    def set_index_file(self, index_file):
        self.index_file = index_file
    
    def get_index_file(self):
        return self.index_file
    
    def set_remote(self, remote):
        self.remote = remote
    
    def get_remote(self):
        return self.remote
    
    def set_local(self, local):
        self.local = local
    
    def get_local(self):
        return self.local

    def _download(self, remote, local):
        if remote.startswith(r"\\"):
            # smb
            copyfile(remote, local)
        elif remote.startswith("http"):
            # http, https
            urllib.urlretrieve (remote, local)
        else:
            # unknown
            if not os.path.isdir(os.path.dirname(local)):
                os.makedirs(os.path.dirname(local))
            copyfile(remote, local)

    def _duplicate(self, local, dup):
        create_symlink(local, dup)

    def _replace_file_with_symlink(self, src, dst):
        remove_file(dst)
        create_symlink(os.path.relpath(src, dst)[3:], dst)

    def create_index(self):
        index = {}
        items = walk_folder(self.dir_path)
        for item in items:
            if os.path.isfile(item):
                hash = md5_file(item)
                if hash not in index.keys():
                    index[hash] = []
                index[hash].append(item)
        with open(self.index_file, 'w') as out_file:
            json.dump(index, out_file, indent=4)

    def download_from_index(self):
        with open(self.index_file) as in_file:
            index = json.load(in_file)
        for file_hash in index.keys():
            remote_file = os.path.join(self.remote, index[file_hash][0])
            local_file = os.path.join(self.local, index[file_hash][0])
            self._download(remote_file, local_file)
            if len(index[file_hash]) > 1:
                for dup in index[file_hash][1:]:
                    dup_file = os.path.join(self.local, dup)
                    self._duplicate(index[file_hash][0], dup_file)

    def reduce_size(self):
        items = walk_folder(self.dir_path)
        for item in items:
            if os.path.isfile(item):
                hash = md5_file(item)
                if hash in self.UNI.keys():
                    self._replace_file_with_symlink(self.UNI[hash], item)
                    if hash in self.DUP.keys():
                        self.DUP[hash].append(item)
                    else:
                        self.DUP[hash] = [item]
                else:
                    self.UNI[hash] = item
        print("DONE")
