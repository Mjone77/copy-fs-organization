# Copy File System Organization
Coppies the organization of one file system to another file system that already contains the data.
Renames and moves files into the same structure as the source directory based on either the size or md5 hash of the files.

## Usage
./organize.py <source dir> <target dir> [--id md5|size]

--id

    The method by which the files are recgonized. md5 uses the md5 hash of the files, size uses the size in bits of the files. Size is much faster, however if two files are the same size then it will not work. md5 is more reliable.