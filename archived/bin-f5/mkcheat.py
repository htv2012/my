#!/usr/bin/env python3
""" Makes a confd.restconf cheatsheet """
import inspect

from confd import restconf


def show_method(name, method):
    try:
        signature = inspect.signature(method)
        print(f"  - {name}{signature}")
    except ValueError:
        # Seems to be a builtin object
        print(f"  - {name} (built-in)")


def show_class(mod, name):
    cls = getattr(mod, name)
    print(f"\n# {name}")
    scope = getattr(cls, "scope", "")
    if scope:
        print(f"\n  - scope: {scope}")

    method_names = [
        name
        for name in dir(cls)
        if not name.startswith("_")
    ]
    methods = {name: getattr(cls, name) for name in method_names}
    methods = {
        name: method
        for name, method in methods.items()
        if callable(method)
    }

    print()
    exclusion = {"make"}
    for name, method in methods.items():
        if name not in exclusion:
            show_method(name, method)


def get_mro(obj):
    try:
        return set(obj.__mro__)
    except AttributeError:
        return set()


def main():
    """ Entry """

    interested = {restconf.AbstractObjectManager, restconf.AbstractManager}
    cls_list = [
        name
        for name in dir(restconf)
        if interested.intersection(get_mro(getattr(restconf, name)))
    ]
    cls_list.remove("AbstractManager")
    cls_list.remove("AbstractObjectManager")

    for name in sorted(cls_list):
        show_class(restconf, name)


if __name__ == '__main__':
    main()
