#!/usr/bin/python3
"""
Reorganizes the target directory to match the file structure and names as the source directory based on checksums.
Usage: ./organize.py -h
"""
from os import walk, makedirs, listdir, rmdir
from os.path import join, isfile, exists as path_exists, dirname, getsize
from shutil import move
from sys import argv, exit
from hashlib import md5
from argparse import ArgumentParser

def organize(args, size):
    """Organizes the target directory to match the file structure of the source directory

    Arguments:
        args {Namespace} -- args.source {str} and args.target {str} are the source and target directories to coppy the file structure from and to, respectively
        size {bool} -- If true -> id files by their size. Else -> id files by their md5 hash
    """
    source_files = {}

    for folder in [args.source, args.target]:
        for subdir, dirs, files in walk(folder):
            for f in files:
                # Set id to either the size of the file or the md5 hash
                if size:
                    id = getsize(join(subdir, f))
                else:
                    id = hash(join(subdir, f))
                if folder == argv[1]:
                    # Add files from source to an array
                    source_files[id] = ({'path': join(subdir[len(argv[1]):], f)})
                else:
                    # Check if hash exists in source_files. If yes -> move and rename to match source
                    if id in source_files:
                        current_path = join(subdir,f)
                        new_path = join(argv[2], source_files[id]['path'])
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

def checkForSizeConflicts(args):
    """Checks if any two files of the same size exist in either the source or target directories

    Arguments:
        args {Namespace} -- args.source {str} and args.target {str} are the two directories to check

    Returns:
        array -- Array containing the two file paths that are found to be the same size, None if no conflicting files found
    """
    for folder in [args.source, args.target]:
        sizes = {}
        for subdir, dirs, files in walk(folder):
            for f in files:
                fpath = join(subdir, f)
                size = getsize(fpath)
                if size in sizes:
                    return [fpath, sizes[size]]
                sizes[size] = fpath
    return None

def hash(fname):
    """Computes the md5 hash of the given file

    Arguments:
        fname {str} -- name of file to hash

    Returns:
        str -- md5 hash of the file
    """
    hash_md5 = md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Parse arguements
parser = ArgumentParser(description='Reorganizes the target directory to match the file structure and names as the source directory based on checksums.')
parser.add_argument('source', type=str, help='the dir to get copy the file structure from.')
parser.add_argument('target', type=str, help='the dir to recreate the file structure in.')
parser.add_argument('-i', '--id', type=str, default='md5', choices=['md5', 'size'], help='The method to id files. md5 id\'s files by their md5 hash and size by their size. First run -s to check if size will work.')
parser.add_argument('-s', '--sizecheck', action='store_true', help='Check if the size id will work. Do not change any files.')
args = parser.parse_args()

# Decide what to do
size = args.id == 'size'
if size or args.sizecheck:
    conflict = checkForSizeConflicts(args)
    if conflict:
        print('Size conflicts exist. Size id will not work.\nConflicting files: '+str(conflict))
        exit()
    else:
        print('No size conflicts exist.')
if not args.sizecheck:
    organize(args, size)