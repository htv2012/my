#!/usr/bin/env python3
"""Create yuml.me diagram"""

import fileinput
import re


def parse_class(text):
    """
    Given a line representing Python class declaration, return the names
    of the parent and child class

    >>> parse_class('class Foo:')
    ['Foo']

    >>> parse_class('class Foo(object):')
    ['Foo']

    >>> parse_class('class Foo(path.to.module.Bar):')
    ['Bar', 'Foo']

    >>> parse_class('class Foo(Base1, Base2):')
    ['Base2', 'Base1', 'Foo']
    """

    hierarchy = reversed(
        [
            t.split(".")[-1]
            for t in re.split(r"[(): ]", text.strip())
            if t not in {"class", "object", ""}
        ]
    )
    hierarchy = list(hierarchy)
    return hierarchy


def format_yuml(classes):
    """Given a list of classes, format them in yUML syntax"""
    return " -> ".join("[{}]".format(c) for c in classes)


def main():
    """Entry point"""
    for classes in map(parse_class, fileinput.input()):
        print(format_yuml(classes))


if __name__ == "__main__":
    main()
