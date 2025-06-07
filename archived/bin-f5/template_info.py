#!/usr/bin/python3
import argparse
import json
import operator
import pathlib


parser = argparse.ArgumentParser()
parser.add_argument(
    "path",
    type=pathlib.Path,
    help="Path to template",
)
options = parser.parse_args()
# print(options)

with open(options.path) as stream:
    template = json.load(stream)
# print(template.keys())


print("VARS")
print("====")
vars_list = sorted(template["vars"], key=operator.itemgetter("field"))
for var_info in vars_list:
    print(f"{var_info['field']}", end="")
    description = var_info.get("doc")
    if description:
        print(f": {description}", end="")
    print()