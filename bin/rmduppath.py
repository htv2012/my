#!/usr/bin/env python3
"""
Takes a path (PATH, CDPATH, INCLUDE, LIB, ...) and remove duplicates while
maintaining the order
"""

import os
import sys


def main():
    """Entry"""
    current_path = sys.argv[1]
    seen = set()
    unique_directories = []

    for directory in current_path.split(os.pathsep):
        if directory not in seen:
            unique_directories.append(directory)
        seen.add(directory)
    print(os.pathsep.join(unique_directories))


if __name__ == "__main__":
    main()
