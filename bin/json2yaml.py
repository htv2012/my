#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Converts a JSON file to YAML format
"""

from __future__ import print_function

import argparse
import json

import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType(mode="r"))
    options = parser.parse_args()

    contents = json.load(options.infile)
    print(yaml.safe_dump(contents, indent=4))
