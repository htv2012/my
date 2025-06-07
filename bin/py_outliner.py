#!/usr/bin/env python3
"""
Show outline of a module
"""

import argparse
import pathlib
import pyclbr


def show(obj, indent=""):
    kind = "class" if isinstance(obj, pyclbr.Class) else "def"
    async_ = ""
    if getattr(obj, "is_async", False):
        async_ = "async "
    print(f"{obj.lineno:>6}: {indent}{async_}{kind} {obj.name}")
    for child in obj.children.values():
        show(child, indent + "    ")


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=pathlib.Path)
    options = parser.parse_args()

    module = options.file.stem
    path = str(options.file.parent)

    objects = pyclbr.readmodule_ex(module, path=[path])
    for obj in objects.values():
        show(obj)


if __name__ == "__main__":
    main()
