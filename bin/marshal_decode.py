#!/usr/bin/env python3
"""
Perform a marshal decoding of a file or standard input
"""

from __future__ import print_function

import argparse
import json
import marshal
import sys


def marshal_decode(stream):
    try:
        while True:
            dict_object = marshal.load(stream)
            yield dict_object
    except EOFError:
        pass


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stream",
        nargs="?",
        type=argparse.FileType(mode="rb"),
        default=sys.stdin,
    )
    options = parser.parse_args()
    return options


def main():
    options = parse_command_line()
    for record in marshal_decode(options.stream):
        print("-" * 80)
        print(json.dumps(record, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
