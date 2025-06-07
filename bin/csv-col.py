#!/usr/bin/env python3
"""Select columns from a CSV file."""

import argparse
import csv
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--include",
    nargs="*",
    action="extend",
)
parser.add_argument(
    "-e",
    "--exclude",
    nargs="*",
    action="extend",
)
parser.add_argument("file", nargs="?")
options = parser.parse_args()
print(options)

rows = [row for row in csv.reader(fileinput.input(options.file))]
