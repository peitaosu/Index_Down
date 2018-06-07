import os, sys, json, optparse
from shutil import copyfile
import urllib
from utils import *

class Index():

    def __init__(self):
        self.dir_path = None
        self.index_file = None
        self.source = None
        self.target = None
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
    
    def set_source(self, source):
        self.source = source
    
    def get_source(self):
        return self.source
    
    def set_target(self, target):
        self.target = target
    
    def get_target(self):
        return self.target

    def _download(self, source, target):
        if source.startswith(r"\\"):
            # smb
            copyfile(source, target)
        elif source.startswith("http"):
            # http, https
            urllib.urlretrieve (source, target)
        else:
            # unknown
            if not os.path.isdir(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            copyfile(source, target)

    def _duplicate(self, target, dup):
        create_symlink(target, dup)

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
            source_file = os.path.join(self.source, index[file_hash][0])
            target_file = os.path.join(self.target, index[file_hash][0])
            self._download(source_file, target_file)
            if len(index[file_hash]) > 1:
                for dup in index[file_hash][1:]:
                    dup_file = os.path.join(self.target, dup)
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

def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--path", dest="path",
                      help="directory path")
    parser.add_option("-i", "--index", dest="index",
                      help="index file")
    parser.add_option("-s", "--source", dest="source",
                      help="source path")
    parser.add_option("-t", "--target", dest="target",
                      help="target path")
    parser.add_option("-c", "--create", dest="create", action="store_true", default=False,
                      help="create index")
    parser.add_option("-d", "--download", dest="download", action="store_true", default=False,
                      help="download from index")
    parser.add_option("-r", "--reduce", dest="reduce", action="store_true", default=False,
                      help="reduce size")
    (options, args) = parser.parse_args()
    if not (options.create or options.download or options.reduce):
        parser.print_help()
        sys.exit(-1)
    return options

if __name__ == "__main__":
    index = Index()
    opt = get_options()

    if opt.path:
        index.set_dir_path(opt.path)
    if opt.index:
        index.set_index_file(opt.index)
    if opt.source:
        index.set_source(opt.source)
    if opt.target:
        index.set_target(opt.target)
    if opt.create:
        index.create_index()
    if opt.download:
        index.download_from_index()
    if opt.reduce:
        index.reduce_size()