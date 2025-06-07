#!/usr/bin/env python3
# whatis: Parse a URL from command line or clipboard
import argparse
import sys
import urllib.parse

from jq import jq


def main():
    """Entry"""
    # Get the URL from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?")
    options = parser.parse_args()

    url = options.url or sys.stdin.read()

    # Parse
    parts = urllib.parse.urlparse(url)

    # Report
    print(f"\n# URL: {url}")
    parts = parts._asdict()
    if parts["query"]:
        query = parts["query"]
        parts["query"] = {
            key: value[0] if len(value) == 1 else value
            for key, value in urllib.parse.parse_qs(query).items()
        }
    jq(parts)


if __name__ == "__main__":
    main()
