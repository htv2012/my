#!/usr/bin/env python3
import argparse

from . import get, rcshell


def main():
    parser = argparse.ArgumentParser(prog="rct")
    parser.add_argument("action", choices=["get", "sh"])
    options, remainder = parser.parse_known_args()
    print(">>>", remainder)

    if options.action == "sh":
        rcshell.main(remainder)
    elif options.action == "get":
        get.main(remainder)


if __name__ == "__main__":
    main()
