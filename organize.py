#!/usr/bin/python3
"""
Reorganizes the target directory to match the file structure and names as the source directory based on checksums
Usage: ./organize.py <source dir> <target dir>
"""
from os import walk, makedirs, listdir, rmdir
from os.path import join, isfile, exists as path_exists, dirname
from shutil import move
from sys import argv, exit
from hashlib import md5

if len(argv) != 3:
    print('Usage: ./organize.py <source dir> <target dir>')
    exit()

def organize():
    source_files = {}

    for folder in argv[1:3]:
        for subdir, dirs, files in walk(folder):
            for f in files:
                md5 = hash(join(subdir, f))
                if folder == argv[1]:
                    # Add files from source to an array
                    source_files[md5] = ({'path': join(subdir[len(argv[1]):], f)})
                else:
                    # Check if hash exists in source_files. If yes -> move and rename to match source
                    if md5 in source_files:
                        current_path = join(subdir,f)
                        new_path = join(argv[2], source_files[md5]['path'])
                        print(current_path + ' --> ' + new_path)
                        if current_path != new_path:
                            # Check if file already exists in new_path. If yes -> rename it
                            if isfile(new_path):
                                move(new_path, new_path+'.old')
                            # Make sure the path exists. If not -> create it
                            new_dir = dirname(new_path)
                            if not path_exists(new_dir):
                                makedirs(new_dir)
                            # Move the file
                            move(current_path, new_path)
                            # If the old directory is now empty -> delete it
                            if len(listdir(subdir)) == 0:
                                rmdir(subdir)

"""
Computes the md5 hash of the given file
"""
def hash(fname):
    hash_md5 = md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

organize()