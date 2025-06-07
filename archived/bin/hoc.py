#!/usr/bin/env python3
"""
Hierarchy of classes

Take input from a command such as:

    grep -r --include='*.py' -E "^\s*class\s+\S+"

and output a csv with 2 columns: child_class, parent_class
"""
import csv
import fileinput
import re
import sys


def parse_class(text):
    """
    Given a line representing Python class declaration, return the names
    of the parent and child class
    """
    parsed = [
        t.split('.')[-1] for t in re.split(r'[(): ]', text.strip())
        if t not in {'class', 'object', ''}
        ]
    if len(parsed) == 1:
        parsed.append('')

    return parsed


def main():
    """ Entry point """
    csv_writer = csv.writer(sys.stdout)
    csv_writer.writerow(['class', 'parent'])
    csv_writer.writerows(map(parse_class, fileinput.input()))


if __name__ == '__main__':
    main()

