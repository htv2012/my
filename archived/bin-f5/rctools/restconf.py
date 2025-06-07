#!/usr/bin/env python3
""" A restconf library """
import argparse
import base64
import cmd
import getpass
import json
import pathlib
import re
import readline
import shlex
import shutil
import ssl
import subprocess
import urllib.request


# Search for the jq tool. JQ_PATH either is the absolute path to
# "jq" or `None`
JQ_PATH = shutil.which("jq")


# ======================================================================
# Support Functions
# ======================================================================
def lookup_resource(resource):
    resource = resource.lstrip("/")

    alias_path = pathlib.Path.home() / ".config/restconf.json"
    if not alias_path.exists():
        return resource

    with open(alias_path) as stream:
        aliases = json.load(stream)

    return aliases.get(resource, resource)


def show_curl(url, creds):
    command = [
        "curl",
        "--silent",
        "--insecure",
        "--user", ":".join(creds),
        "--header", 'Accept: application/yang-data+json',
        "--url", url
    ]
    print(" ".join(shlex.quote(token) for token in command))


def get(url, creds):
    """ GET the resources, with caching """
    auth = base64.encodebytes(":".join(creds).encode("utf-8")).decode("utf-8").rstrip()
    headers = {
        "Accept": "application/yang-data+json",
        "Authorization": f"Basic {auth}",
    }
    request = urllib.request.Request(url, headers=headers)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        response = urllib.request.urlopen(request, context=ctx)
        return response
    except urllib.error.HTTPError as error:
        print(f"{error.code} {error.reason}")
        return None


def post(url, payload, creds):
    auth = base64.encodebytes(":".join(creds).encode("utf-8")).decode("utf-8").rstrip()
    headers = {
        "Accept": "application/yang-data+json",
        "Authorization": f"Basic {auth}",
    }
    request = urllib.request.Request(url, headers=headers, data=payload)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        response = urllib.request.urlopen(request, context=ctx)
        return response
    except urllib.error.HTTPError as error:
        print(f"{error.code} {error.reason}")
        return None


def pretty_json(json_object):
    """ Pretty prints a JSON object """
    text = json.dumps(json_object, indent=2, sort_keys=True)
    if JQ_PATH:
        with subprocess.Popen([JQ_PATH, "."], stdin=subprocess.PIPE, encoding="utf-8") as process:
            process.communicate(text)
    else:
        print(text)

# ======================================================================
# RESTCONF Functions
# ======================================================================
def creat_tenant():
    print("create tenant")
