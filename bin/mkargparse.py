#!/usr/bin/env python3
"""Create argparser."""

import sys


def main():
    """Entry"""
    print("import argparse")
    print()
    print("parser = argparse.ArgumentParser()")

    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            args = [f'"{arg[1:3]}"', f'"{arg}"']
        else:
            args = [f'"{arg}"']

        print(f"parser.add_argument({', '.join(args)})")

    print("options = parser.parse_args()")


if __name__ == "__main__":
    main()
