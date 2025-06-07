#!/usr/bin/env python3
"""
Displays the path with markers to indicate duplications

# How do I mark duplicate paths?

Duplicate paths are marked with markers such as A, B, C, ... To achieved
this goal, I create a defaultdict in which the keys are the paths and
the values are the marker.
"""

import argparse
import os
from collections import Counter, defaultdict


def parse_command_line():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("paths")
    options = parser.parse_args()
    return options


def main():
    """Entry point"""
    options = parse_command_line()
    paths = options.paths.split(os.pathsep)

    counts = Counter(paths)
    char_markers = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    markers = defaultdict(lambda: next(char_markers))

    for path in paths:
        if counts[path] > 1:
            print(f"{markers[path]} {path}")
        else:
            print(f"  {path}")


if __name__ == "__main__":
    main()
