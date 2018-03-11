import os, shutil, hashlib

def create_symlink(src, dst):
    os.symlink(src, dst)

def copy_file(src, dst):
    shutil.copyfile(src, dst)

def remove_file(src):
    os.remove(src)

def sha1_file(src):
    sha1 = hashlib.sha1()
    for line in open(src, 'rb'):
        sha1.update(line)
    return sha1.hexdigest()

def sha256_file(src):
    sha256 = hashlib.sha256()
    for line in open(src, 'rb'):
        sha256.update(line)
    return sha256.hexdigest()

def md5_file(src):
    md5 = hashlib.md5()
    for line in open(src, 'rb'):
        md5.update(line)
    return md5.hexdigest()

def walk_folder(dir):
    items = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            items.append(os.path.join(root, name))
    return items
