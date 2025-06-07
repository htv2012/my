#!/usr/bin/env python3
"""
Given a directory or a python file, find the name of the python package
"""

import argparse
import pathlib

marker = "__init__.py"


def find_package(path_to_leaf):
    path = pathlib.Path(path_to_leaf).resolve()
    components = []

    # Leaf is a Python file, not a dir
    if path.is_file() and path.suffix in {".py", ".pyc"}:
        components.append(path.stem)
        path = path.parent

    while (path / marker).exists():
        components.insert(0, path.name)
        path = path.parent

    return ".".join(components)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", default=["."])
    options = parser.parse_args()
    for path in options.paths:
        package = find_package(path)
        if package:
            print(package)
