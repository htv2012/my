#!/usr/bin/env python3
"""
Tally the imports from a root directory
"""

import argparse
import collections
import logging
import os
import pathlib

logging.basicConfig(level=os.getenv("LOGLEVEL", "WARN"))


def count_imports_in_single_file(path):
    counter = collections.Counter()
    logging.debug("path: %s", path)
    with open(path, "r", encoding="utf-8") as stream:
        for line in stream:
            if line.startswith(("from ", "import ")):
                tokens = line.split()
                name = tokens[1]
                counter[name] += 1
    return counter


def count_imports(root: str):
    counter = collections.Counter()
    root = pathlib.Path(root)
    for path in root.rglob("*.py"):
        counter.update(count_imports_in_single_file(path))

    return counter


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+")
    options = parser.parse_args()

    counter = collections.Counter()

    for root in options.roots:
        counter.update(count_imports(root))

    for name, count in counter.most_common():
        print(f"{count:>4} {name}")


if __name__ == "__main__":
    main()
