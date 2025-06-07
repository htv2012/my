#!/usr/bin/env python3
import base64
import collections
import csv
import email
import itertools
import functools
import json
import os
import pathlib
import pprint
import shutil
import ssl
import subprocess
import sys
import types
import urllib.request


# Fixed up the PYTHONPATH (sys.path)
here = pathlib.Path("~/code/systest-common").expanduser()
sys.path.append(str(here))
sys.path.append(str(here / "libs"))
sys.path.append(str(here / "tests"))

# These imports depends on the updated sys.path
import systestcommon
from systestcommon import nginx
from systestcommon import utils
from systestcommon.nginx.api.rbac.role import Permission, Role
from systestcommon.nginx.api.rbac.user import User
from systestcommon.nginx.api.environment import Environment
from tests import testers


# ======================================================================
# Generics
# ======================================================================
def jq(obj, jq_expression="."):
    """Print a JSON object."""
    global JQ
    text = json.dumps(obj, indent=4)
    if JQ:
        subprocess.run(["jq", jq_expression], input=text, encoding="utf-8")
    else:
        print(text)


def display_hook(value):
    """Display a nicer repr."""
    if value is None:
        return
    pprint.pprint(value, indent=4)
    __builtins__._ = value


def source(path):
    """Source a file into the global namespace."""
    with open(path, "r", encoding="utf-8") as stream:
        raw_code = stream.read()
    exec(raw_code, globals())


# ======================================================================
# systest-common specifics
# ======================================================================
def get_symbols(symbols_path=None):
    """Get the symbols to look up the controller's host IP address."""
    if symbols_path is None:
        symbols_path = os.getenv("TESTRUN_SYMBOLS") or os.getenv("SYSTEST_SYMBOLS")

    try:
        with open(symbols_path, "r", encoding="utf-8") as stream:
            symbols = json.load(stream)
            symbols = types.SimpleNamespace(**symbols)
    except TypeError:
        print(
            "Please set either TESTRUN_SYMBOLS or SYSTEST_SYMBOLS"
            " pointing to the symbols.json file."
        )
        sys.exit(1)

    return symbols


def make_api(host, username, password):
    """Create an API function."""
    root = f"https://{host}"
    ssl_context = ssl.SSLContext()
    auth = f"{username}:{password}".encode("utf-8")
    auth = base64.b64encode(auth).decode("utf-8")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
    }

    def api(method, path, payload=None):
        """Make an API call."""
        url = f"{root}/{path.strip('/')}"
        request = urllib.request.Request(
            url, data=payload, headers=headers, method=method.upper()
        )
        try:
            response = urllib.request.urlopen(request, context=ssl_context)
            return response
        except urllib.error.HTTPError as error:
            return error

    def get(path):
        return api("get", path)

    def post(path, payload):
        return api("post", path, payload)

    def put(path, payload):
        return api("put", path, payload)

    def delete(path):
        return api("delete", path)

    return api, get, post, put, delete


# ======================================================================
# main
# ======================================================================
JQ = shutil.which("jq")
sys.displayhook = display_hook

# Source the test env
test_env_file = pathlib.Path("~/.testenv/set_stack_id.sh").expanduser()
if test_env_file.exists():
    for line in test_env_file.open():
        key, value = line.strip().replace("export ", "").split("=")
        os.environ[key] = value

symbols = get_symbols()
api, get, post, put, delete = make_api(
    host=symbols.control_host_ips[0],
    username=symbols.ctrl_admin_username,
    password=symbols.ctrl_admin_pass,
)

# Create a few objects
session = systestcommon.utils.testsession.TestSession()
cluster = systestcommon.nginx.cluster.Cluster(session.symbols, session.bigip_symbols)
ctrl = cluster.ctrl
ctrl.instances.refresh()

print("Objects created: session, cluster, ctrl, symbols, api")

for path in sys.argv[1:]:
    source(path)
