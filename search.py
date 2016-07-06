# Search for eligable files

from __future__ import print_function
import os.path
import re
import os

def find(root, reg):

    if not os.path.isdir(root):
        raise(Exception("Root is not a directory: %s" % root))

    # could use os.walk, but oh well we can ignore .files this way
    for entry in os.listdir(root):
        if not entry[:1] == ".":
            entry_path = os.path.join(root, entry)
            if os.path.isdir(entry_path):
                for loop in find(entry_path, reg):
                    yield loop
            elif reg.match(entry_path):
                yield entry_path

# if __name__ == '__main__':
#     root = os.path.dirname(__file__)
#     for file_ in find(root, re.compile(r"^.+\.mov$", re.I)):
#         print(file_)
