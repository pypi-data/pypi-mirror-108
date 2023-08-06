from os import listdir
from os import walk

def mapper(src_dir: str):
    f = []
    d = []
    for (dirpath, dirnames, filenames) in walk(src_dir):
        f.extend(filenames)
        d.extend(dirnames)
        d.extend(dirpath)
        break
    return (f,d)