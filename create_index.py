import os, sys, json
from utils import *

def create_index(dir_path):
    index = {}
    items = walk_folder(dir_path)
    for item in items:
        if os.path.isfile(item):
            hash = md5_file(item)
            if hash not in index.keys():
                index[hash] = []
            index[hash].append(item)
    return index

def save_index(index, index_file):
    with open(index_file, 'w') as out_file:
        json.dump(index, out_file, indent=4)

if __name__ == "__main__":
    dir_path = "."
    index_file = "down.index"
    if len(sys.argv) == 1:
        print("> python create_index.py <dir_path> [<index_file>]")
        print("Please provide directory path which you want to create index.")
        sys.exit(-1)
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    if len(sys.argv) > 2:
        index_file = sys.argv[2]
    index = create_index(dir_path)
    save_index(index, index_file)