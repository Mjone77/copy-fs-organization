# Copy File System Organization
Coppies the organization of one file system to another file system that already contains the data.
Renames and moves files into the same structure as the source directory based on either the size or md5 hash of the files.

## Usage
organize.py [-h] [-i {md5,size}] [-s] source target

Reorganizes the target directory to match the file structure and names as the
source directory based on checksums.

positional arguments:

  source                the dir to get copy the file structure from.

  target                the dir to recreate the file structure in.


optional arguments:

  -h, --help

                        show this help message and exit

  -i {md5,size}, --id {md5,size}

                        The method to id files. md5 id's files by their md5 hash and size by their size. First run -s to check if size will work.

  -s, --sizecheck

                        Check if the size id will work. Do not change any files.