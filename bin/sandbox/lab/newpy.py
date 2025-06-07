#!/usr/bin/env python3
"""Create a new Python project using flit."""

import argparse
import os
import pathlib


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=pathlib.Path)
    parser.add_argument("-d", "--description", default="A package.")
    options = parser.parse_args()

    dest = options.dir
    dest.mkdir(exist_ok=True)
    os.chdir(dest)
    package_dir = pathlib.Path(dest.name)
    package_dir.mkdir(exist_ok=True)

    init_file = package_dir / "__init__.py"
    init_file.write_text(f'"""{options.description}"""\n__version__ = "0.1"\n')


if __name__ == "__main__":
    main()
