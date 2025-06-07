#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "prettytable",
# ]
# ///
import argparse
import csv
import fileinput
import io

import prettytable


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--header", action=argparse.BooleanOptionalAction, default=True)
    options = parser.parse_args()
    print(options)

    buffer = io.StringIO()
    for line in fileinput.input(options.file):
        buffer.write(line)
    buffer.seek(0)

    # Determine the header (field_names)
    field_names = None
    field_names = next(csv.reader(buffer))
    if not options.header:
        buffer.seek(0)
        field_names = [f"F{i + 1}" for i, _ in enumerate(field_names)]

    print(buffer.tell())
    table = prettytable.from_csv(buffer, field_names=field_names)
    table.align = "l"
    text = table.get_string()
    print(text)


if __name__ == "__main__":
    main()
