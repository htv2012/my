#!/usr/bin/env python3
"""
Given a JSON object, traverse to all the leaf nodes
"""

import argparse
import fileinput
import json


def generate_paths(obj, path=None):
    path = path or tuple()

    if isinstance(obj, list) and not isinstance(obj, str):
        for index, value in enumerate(obj):
            yield from generate_paths(value, path + (index,))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            yield from generate_paths(value, path + (key,))
    else:
        yield path, obj


def path2jsonpath(path):
    path = [f"[{p}]" if isinstance(p, int) else f".{p}" for p in path]
    path = "".join(path)
    return path.lstrip(".")


def path2str(path):
    path = "/".join(str(p) for p in path)
    return path


def path2index(path):
    path = "".join(f"[{p!r}]" for p in path)
    return path


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file-path",
        dest="format",
        action="store_const",
        const="file-path",
        default="json-path",
        help="Output format: path with slashes as separator",
    )
    parser.add_argument(
        "-j",
        "--json-path",
        dest="format",
        action="store_const",
        const="json-path",
        help="Output format: jsonpath",
    )
    parser.add_argument(
        "-i",
        "--index-path",
        dest="format",
        action="store_const",
        const="index-path",
        help="Output format: index notation",
    )
    options, args = parser.parse_known_args()

    input_text = "".join(line for line in fileinput.input(args))
    json_object = json.loads(input_text)

    path_transformer = {
        "file-path": path2str,
        "json-path": path2jsonpath,
        "index-path": path2index,
    }[options.format]

    for path, value in generate_paths(json_object):
        key = path_transformer(path)
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
