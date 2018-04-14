import os, sys
from utils import *

UNI = {}
DUP = {}

def replace_file_with_symlink(src, dst):
    remove_file(dst)
    create_symlink(src, dst)

def reduce_size(dir_path):
    items = walk_folder(dir_path)
    for item in items:
        if os.path.isfile(item):
            hash = md5_file(item)
            if hash in UNI.keys():
                replace_file_with_symlink(UNI[hash], item)
                if hash in DUP.keys():
                    DUP[hash].append(item)
                else:
                    DUP[hash] = [item]
            else:
                UNI[hash] = item
    print 'DONE.'

if __name__ == "__main__":
    dir_path = '.'
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    reduce_size(dir)