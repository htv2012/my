import collections
import csv
import itertools
import json
import os
import pathlib
import pprint
import shutil
import subprocess
import sys

# Load objexplore, which could fail
JQ = shutil.which("jq")
try:
    from objexplore import explore as e
except ImportError:
    pass


def jq(value):
    try:
        display = json.dumps(value, indent=4, sort_keys=True)
        if JQ:
            process = subprocess.Popen(
                [JQ, "."],
                stdin=subprocess.PIPE,
                encoding="utf-8",
            )
            process.communicate(display)
        else:
            print(display)
    except TypeError:
        # value cannot be presented in JSON
        pprint.pprint(value)

def display_hook(value):
    if value is None:
        return

    pprint.pprint(value)


    __builtins__._ = value



if __name__ == '__main__':
    if sys.version_info.major == 2:
        sys.exit()

    sys.displayhook = display_hook
    print('To customize this environment, edit', __file__)

