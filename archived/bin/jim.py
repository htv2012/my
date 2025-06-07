#!/usr/bin/env python
from __future__ import print_function
import sys


if __name__ == '__main__':
    terms = sys.argv[1:]
    imports_filename = __file__.replace('.py', '.txt').replace('bin', 'etc')

    with open(imports_filename) as f:
        found = set()
        found = set(line for line in f if any(term in line for term in terms))
        print(''.join(sorted(found)))

