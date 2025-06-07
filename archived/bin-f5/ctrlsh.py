#!/usr/bin/env python3
"""Ctrl Shell."""
import argparse
import cmd
import json
import logging
import os
import pathlib
import readline
import shlex
import shutil
import subprocess
import tempfile
import types

import urllib3
import requests

# TODO: Disable ctrl+C


PATH_ENVIRONMENT = "services/environments"


logging.basicConfig(level=os.getenv("LOGLEVEL", "WARN"))
LOGGER = logging.getLogger()


def show_json(data):
    jq = shutil.which("jq")
    text = json.dumps(data, indent=4, sort_keys=True)
    if jq is None:
        print(text)
        return

    subprocess.run(["jq", "."], input=text, encoding="utf-8")


def _confirm(message, data):
    print(message)
    show_json(data)
    answer = input("Press Y to confirm, N to cancel: ")
    return answer.upper() == "Y"


class NginxApi:
    def __init__(self, symbols):
        self.symbols = symbols
        self.session = requests.Session()
        self.session.verify = False

    def login(self):
        url = self._url("platform/login")
        LOGGER.info(
            "Logging in using email %r and password %r",
            self.symbols.ctrl_admin_email,
            self.symbols.ctrl_admin_pass,
        )
        LOGGER.info("URL=%r", url)
        payload = {
            "credentials": {
                "username": self.symbols.ctrl_admin_email,
                "password": self.symbols.ctrl_admin_pass,
                "type": "BASIC",
            }
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()

    def get(self, path):
        url = self._url(path)
        response = self.session.get(url)
        return response

    def create_environment(self, payload):
        url = self._url(PATH_ENVIRONMENT)
        response = self.session.post(url=url, json=payload)
        return response

    def delete_environment(self, name):
        url = self._url(f"{PATH_ENVIRONMENT}/{name}")
        response = self.session.delete(url)
        response.raise_for_status()

    def _url(self, path):
        path = path.strip("/")
        url = f"https://{self.symbols.control_host_ips[0]}/api/v1/{path}"
        return url


class Shell(cmd.Cmd):
    prompt = "ctrlsh> "

    def __init__(self, api, completekey="tab", stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.api = api

    def do_history(self, param):
        count = readline.get_current_history_length()
        for index in range(1, count + 1):
            history_item = readline.get_history_item(index)
            print(f"{index} {history_item}")

    def do_get(self, args):
        response = self.api.get(args)
        output = response.json()
        show_json(output)

    def do_env(self, args):
        """Perform actions on environments."""
        tokens = shlex.split(args)
        subcmd = tokens.pop(0)
        method = getattr(self, f"env_{subcmd}", None)
        if method is None:
            print(f"env sub-command not found: {subcmd}")
            return
        method(*tokens)

    def env_ls(self, *args):
        """List the environments."""
        response = self.api.get(PATH_ENVIRONMENT)
        output = response.json()
        for entry in output["items"]:
            print(entry["metadata"]["name"])

    def env_get(self, *args):
        """Get a particular environment."""
        response = self.api.get(f"{PATH_ENVIRONMENT}/{args[0]}")
        show_json(response.json())

    def env_create(self, *args):
        """Create an environment."""
        temp_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        temp_file.close()
        payload = {
            "metadata": {
                "name": "env_name",
                "displayName": "My Environment",
                "description": "This is a test environment",
                "tags": ["tag1", "tag2"],
            },
            "desiredState": {},
        }
        with open(temp_file.name, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=4)
        subprocess.run(["vim", temp_file.name])

        # Watch for invalid JSON
        with open(temp_file.name, "r", encoding="utf-8") as stream:
            raw = stream.read()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as error:
            for line_number, line in enumerate(raw.splitlines(), 1):
                print(f"{line_number:>4} {line}")
            print("---")
            print(error)
            print("Environment not created")
            return

        # Confirm
        if _confirm("Create an environment with the following payload.", payload):
            response = self.api.create_environment(payload)
            show_json(response.json())

    def env_delete(self, name, *args):
        """Delete an environment."""
        self.api.delete_environment(name)

    def emptyline(self) -> bool:
        """Prevent empty line from repeating previous command."""
        pass

    def do_exit(self, args):
        """Exit the shell."""
        return True

    # Aliases
    do_EOF = do_exit
    do_h = do_history
    do_q = do_exit
    do_quit = do_exit
    env_rm = env_delete


def main():
    """Entry"""
    urllib3.disable_warnings()

    symbols_file = os.getenv("TESTRUN_SYMBOLS")
    if symbols_file is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("symbols_file")
        options = parser.parse_args()
        symbols_file = options.symbols_file

    with open(symbols_file, encoding="utf-8") as stream:
        symbols = json.load(stream)
        symbols = types.SimpleNamespace(**symbols)

    # Load history
    history_path = pathlib.Path("~/.ctrlsh_history").expanduser()
    if history_path.exists():
        readline.read_history_file(history_path)

    try:
        api = NginxApi(symbols)
        api.login()
        shell = Shell(api)
        shell.cmdloop("Welcome to the Controller Shell, type help for more information.")
    finally:
        readline.write_history_file(history_path)


if __name__ == "__main__":
    main()
