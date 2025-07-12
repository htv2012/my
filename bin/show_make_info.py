#!/usr/bin/env python3
"""Show Makefile Information."""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "prettytable",
# ]
# ///

import atexit
import bisect
import csv
import os
import re
import subprocess
import tempfile

import prettytable


def print_table(headers, rows):
    table = prettytable.PrettyTable()
    table.align = "l"
    table.field_names = headers
    table.add_rows(rows)
    print(table)


def show_dependency(makefile_path: str):
    """Show the targets and dependencies.

    :param makefile: The path to the Makefile
    """
    # print("\n#\n# Targets and Dependencies\n#\n")
    target_pattern = re.compile(r"^\w+:[^:]+$")
    target_description = []

    with open(makefile_path, "r", encoding="utf-8") as stream:
        for line in stream:
            if line.startswith("###"):
                description = line.removeprefix("###").strip()
            elif target_pattern.match(line):
                target = line.strip()
                bisect.insort(target_description, (target, description))

    print("Targets:")
    print_table(("Target", "Description"), target_description)


def show_vars(makefile_path):
    """Show variables and values."""
    with open(makefile_path, "r", encoding="utf-8") as stream:
        contents = stream.read()
    var_names = re.findall(r"^(\w+)\s+[:?]*=", contents, re.MULTILINE)
    if not var_names:
        return

    # Create a temp makefile which prints the values of all
    # variables in CSV format
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
        atexit.register(os.unlink, file.name)
        file.write(".PHONY: debug\n")
        file.write("include Makefile\n")
        file.write("debug:\n")
        for name in sorted(var_names):
            file.write(f'\t@echo "{name}","$({name})"\n')
    process = subprocess.run(["make", "-f", file.name, "debug"], capture_output=True, text=True)

    # Parse the CSV output
    reader = csv.reader(process.stdout.splitlines())
    rows = list(reader)

    print()
    print("Variables:")
    print_table(("Variable", "Value"), rows)


def main():
    """Entry"""
    show_dependency("Makefile")
    show_vars("Makefile")


if __name__ == "__main__":
    main()
