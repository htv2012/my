#!/usr/bin/env python3
"""
A Python skeleton script
"""
import collections
import contextlib
import csv
import dataclasses
import itertools
import json
import os
import pathlib
import pprint
import readline
import shutil
import subprocess
import sys

import requests

from systestcommon import nginx
from systestcommon import utils
from systestcommon import workloads
from systestcommon.nginx.api.application import Application
from systestcommon.nginx.api.environment import Environment
from systestcommon.nginx.api.gateway import Gateway
from tests import testers
import systestcommon


def jq(json_object, filter="."):
    """Display JSON object using jq tool."""
    text = json.dumps(json_object, indent=4, sort_keys=True)
    jq = shutil.which("jq")
    if jq is None:
        print(text)
        return

    subprocess.run(["jq", filter], input=text, encoding="utf-8")


def mkenv(name, display_name=None, description=None, tags=None):
    global ctrl

    try:
        env = Environment(ctrl, name, display_name, description, tags)
        env.create()
    except nginx.api.exceptions.EnvironmentCreateError:
        env = Environment(ctrl, name)
        env.refresh()
        pass
    return env


def mkapp(env, name, display_name=None, description=None, tags=None):
    app = Application(env, name, display_name, description, tags)
    try:
        app.create()
    except nginx.api.exceptions.ApplicationCreateError:
        app.refresh()
    return app


def mkgateway(
    env,
    name,
    placement=None,
    uris=None,
    display_name=None,
    description=None,
    tags=None,
    methods=None,
    global_tls=None,
    client_max_body_size=None,
    allow_underscores_in_headers=None,
    receive_buffer_size=None,
    send_buffer_size=None,
    tcp_keepalive=None,
    error_set_ref=None,
    client=None,
    type1_directives=None,
    ha=None,
):
    global ctrl

    if placement is None:
        placement = {"instanceRefs": [{"ref": ctrl.instances[0].instance_ref}]}

    if uris is None:
        uris = {f"http://example.com": {}}

    gateway = Gateway(
        env,
        name,
        placement,
        uris,
        display_name,
        description,
        tags,
        methods,
        global_tls,
        client_max_body_size,
        allow_underscores_in_headers,
        receive_buffer_size,
        send_buffer_size,
        tcp_keepalive,
        error_set_ref,
        client,
        type1_directives,
        ha,
    )
    try:
        gateway.create()
    except nginx.api.exceptions.GatewayCreateError:
        gateway.refresh()
    return gateway


def cheat():
    print("Packages imported: systestcommon, nginx, testers, utils, workloads")
    print("Objects created: cluster, ctrl, and session")
    print("Helpful functions: jq, mkenv, mkapp, mkgateway, source")


def source(path):
    """Source the file, similar to bash."""
    with open(path, encoding="utf-8") as stream:
        code_snippet = stream.read()
    exec(code_snippet, globals())


class Api:
    def __init__(self, control_host_ip):
        self.control_host_ip = control_host_ip
        self.sess = requests.Session()
        self.sess.verify = False
        self.resp = None

    def _url(self, path):
        path = path.lstrip("/")
        return f"https://{self.control_host_ip}/api/v1/{path}"

    def show_json(self, resp):
        if resp.status_code == 204:
            return
        jq(resp.json())

    def get(self, path):
        self.resp = self.sess.get(self._url(path))
        self.resp.raise_for_status()
        # self.show_json(self.resp)
        return self.resp.json()

    def post(self, path, payload):
        self.resp = self.sess.post(self._url("platform/login"), json=payload)
        self.resp.raise_for_status()
        self.show_json(self.resp)

    def login(self):
        self.post(
            "platform/login",
            payload={
                "credentials": {
                    "username": "admin@nginx.test",
                    "password": "Testenv12#",
                    "type": "BASIC",
                }
            },
        )


#
# Main - Do not wrap in if __name__ == "__main__"
#

# Sanity
if "SYSTEST_SYMBOLS" not in os.environ:
    raise SystemExit("Please set env var SYSTEST_SYMBOLS")

session = systestcommon.utils.testsession.TestSession()
cluster = systestcommon.nginx.cluster.Cluster(session.symbols, session.bigip_symbols)
ctrl = cluster.ctrl
ctrl.instances.refresh()

api = Api(session.symbols["control_host_ips"][0])
api.login()

print("Welcome to the System-common Shell")
cheat()
