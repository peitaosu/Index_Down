import os, shutil, hashlib

def create_symlink(src, dst):
    os.symlink(src, dst)

def copy_file(src, dst):
    shutil.copyfile(src, dst)

def sha1_file(src):
    sha1 = hashlib.sha1()
    with open(src, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()