#!/usr/bin/env python3
"""
This utility formats a markdown table
"""

import argparse
import csv
import fileinput
import sys


def split_into_columns(text):
    """
    Splits a markdown table row into columns

    :param text: A string representing a table row, e.g. "| col1 | col2 |"
    :return: A list of strings, e.g. ['col1', 'col2']
    """
    row = [cell.strip() for cell in text.strip().strip("|").split("|")]
    return row


def adjust_alignment(widths, old_separators):
    """
    Given a list of widths which represents the widths of each column,
    and a a list of separators, return a list of format strings for each
    column and a list of separators

    :param widths: A list of widths, e.g. [4, 7]
    :param old_separators: A list of separators, e.g. ['--', '--:']
    :return Two lists. The first is a list of cell formats, e.g.
        ['{:<4}', '{:>7}'] and a list of new separators, e.g.
        ['----', '------:']
    """
    alignments = []
    new_separators = []
    for width, dashes in zip(widths, old_separators):
        if dashes[0] == ":" and dashes[-1] == ":":
            # Center justify
            alignments.append("{:^%d}" % width)
            new_separators.append(":" + "-" * (width - 2) + ":")
        elif dashes[-1] == ":":
            # Right justify
            alignments.append("{:>%d}" % width)
            new_separators.append("-" * (width - 1) + ":")
        else:
            # Left justify
            alignments.append("{:<%d}" % width)
            new_separators.append("-" * width)

    return alignments, new_separators


def format_md_table(lines, output_file=None):
    """
    Given a list of lines representing the old table, reformat it with
    proper alignments.

    :param lines: Any iterable representing a list of lines
    :output_file: A file handle, if not supplied, the output will be
        written out to sys.stdout
    """
    output_file = output_file or sys.stdout

    rows = list(map(split_into_columns, lines))
    widths = [max(map(len, column)) for column in zip(*rows)]
    fmts, rows[1] = adjust_alignment(widths, rows[1])
    fmt = "| " + " | ".join(fmts) + " |"

    for row in rows:
        output_file.write(fmt.format(*row))
        output_file.write("\n")


def format_csv_table(rows, output_file=None):
    output_file = output_file or sys.stdout
    rows = list(rows)
    widths = [max(map(len, column)) for column in zip(*rows)]

    separators = ["-" * w for w in widths]
    rows.insert(1, separators)
    fmt = "| " + " | ".join("{:<%d}" % w for w in widths) + " |"

    for row in rows:
        output_file.write(fmt.format(*row))
        output_file.write("\n")


def main():
    """Entry"""
    parser = argparse.ArgumentParser("mdtable")
    parser.add_argument("-i", "--input", choices=["md", "tsv", "csv"], default="md")
    options, args = parser.parse_known_args()
    lines = fileinput.input(args)

    if options.input == "md":
        format_md_table(lines)
    else:
        delimiter = "," if options.input == "csv" else "\t"
        reader = csv.reader(lines, delimiter=delimiter, skipinitialspace=True)
        format_csv_table(reader)


if __name__ == "__main__":
    main()
