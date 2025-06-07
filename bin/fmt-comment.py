#!/usr/bin/env python3
"""Script to reformat the comments."""

import argparse
import fileinput
import itertools
import textwrap


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", type=int, default=72)
    options, args = parser.parse_known_args()

    lines = list(fileinput.input(args))
    indent = "".join(itertools.takewhile(lambda c: c == " " or c == "#", lines[0]))
    width = options.width - len(indent)

    text = "\n".join(line.strip().lstrip("#").strip() for line in lines)
    text = textwrap.fill(
        text, width=width, initial_indent=indent, subsequent_indent=indent
    )
    print(text)


if __name__ == "__main__":
    main()
