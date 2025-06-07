#!/usr/bin/env python3
""" A restconf shell """
import argparse
import cmd
import getpass
import json
import pathlib
import readline
import shlex
import shutil
import subprocess

from . import restconf


INTRODUCTION = """
Welcome to the restconf shell, type help to get started
Sample commands:
    ls                       # List sub dir, 1 level deep
    cd f5-cluster:cluster    # Just like bash
    get                      # GET current directory location
    get /f5-cluster:cluster  # GET at a different location

Please do not 'get' from the root, there is a bug which will bite ya!
"""


class RestconfShell(cmd.Cmd):
    """ A restconf shell """
    intro = INTRODUCTION

    def __init__(self, ip_address, creds):
        super().__init__()
        self.creds = creds
        self.root = f"https://{ip_address}:8888/restconf/data"
        self.cwd = pathlib.Path("/")
        self.cache = {}
        self._ip_address = ip_address
        self._set_prompt()

    def _set_prompt(self):
        self.prompt = f"\n{self._ip_address}:{self.cwd}\nrestconf> "

    def do_get(self, args):
        """
        Performs a GET on a resource

        Examples:

            get  # Get resources at the curent dir
            get /f5-portgroup:portgroups  # Gets at a specific resource
            get /f5-portgroup:portgroups -o /tmp/output.json
        """

        # Parses the command line
        args = shlex.split(args)
        parser = argparse.ArgumentParser(prog="get")
        parser.add_argument("-o", "--output")
        parser.add_argument("resource")
        try:
            options = parser.parse_args(args)
        except SystemExit:
            parser.print_usage()
            return

        url = self._get_url_from_resource(options.resource)
        restconf.show_curl(url, self.creds)
        response = restconf.get(url, creds=self.creds)
        if response is None:
            return

        print(f"{response.status} {response.reason}")

        if response.status == 204:
            # No content
            return

        try:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
            restconf.pretty_json(data)
        except json.decoder.JSONDecodeError as error:
            print(f"Malformed JSON returned: {error}")
            for line_number, line in enumerate(raw.splitlines(), 1):
                print(f"{line_number:>3}: {line}")

        if options.output:
            with open(options.output, "w") as stream:
                json.dump(data, stream, indent=2, sort_keys=True)
            print(f"Output saved to {options.output}")

    def do_post(self, args):
        # Parses the command line
        args = shlex.split(args)
        parser = argparse.ArgumentParser(prog="post")
        # TODO: Do not require payload, but allow editing using $EDITOR
        parser.add_argument("-p", "--payload", type=argparse.FileType("r"), required=True)
        parser.add_argument("resource")
        try:
            options = parser.parse_args(args)
        except SystemExit:
            parser.print_usage()
            return

        url = self._get_url_from_resource(options.resource)
        payload = json.load(options.payload)
        print(f"POST {url}")
        print("Payload:")
        restconf.pretty_json(payload)
        print()

        payload = json.dumps(payload).encode("utf-8")
        response = restconf.post(url, payload, self.creds)
        if response is None:
            return

    def _list_files(self, arg):
        url = f"{self.root}{self.cwd}".rstrip("/")
        url = f"{url}/{arg.strip()}".rstrip("/")
        url = f"{url}?depth=1"

        response = restconf.get(url, creds=self.creds)
        if response is None:
            return []

        data = json.load(response)
        json_object = next(iter(data.values()))
        return list(json_object)

    def do_ls(self, arg):
        """Lists sub directories"""
        for subdir in self._list_files(arg):
            print(subdir)

    def do_cd(self, subdir: str):
        """Changes directory"""
        old_cwd = self.cwd
        if subdir.startswith("/"):
            self.cwd = pathlib.Path(subdir)
        else:
            self.cwd = self.cwd / subdir
            self.cwd = self.cwd.resolve()

        if old_cwd == self.cwd:
            return

        # Test for valid dir
        if restconf.get(f"{self.root}{self.cwd}", creds=self.creds) is not None:
            self.do_ls("")
            return

        self.cwd = old_cwd

    def complete_cd(self, text, line, begidx, endidx):
        all_subdirs = self._list_files("")
        chosen = [d for d in all_subdirs if d.startswith(text)]
        return chosen

    def do_exit(self, unused_param):
        """Exits the shell"""
        return True

    def do_history(self, param):
        count = readline.get_current_history_length()
        for index in range(1, count+1):
            history_item = readline.get_history_item(index)
            print(f"{index} {history_item}")

    def default(self, line):
        line = line.strip()
        if self.expand_history(line):
            return

        print(f"Unknown syntax: {line}")

    def expand_history(self, line):
        """
        Handles "!n" where n is an integer
        """
        try:
            index = int(line.lstrip("!"))
        except ValueError:
            return False

        history_item = readline.get_history_item(index)
        print(history_item)
        self.onecmd(history_item)

        # Replace !N with actual history item
        history_number = readline.get_current_history_length()
        readline.replace_history_item(history_number - 1, history_item)
        return True

    do_q = do_exit
    do_EOF = do_exit

    def emptyline(self):
        """ Prevents empty lines from executing previous command """

    def postcmd(self, stop, line):
        self._set_prompt()
        return stop

    def _get_url_from_resource(self, resource):
        if resource.startswith("/"):
            url = f"{self.root}{resource}"
        else:
            url = f"{self.root}{self.cwd}".rstrip("/")
            url = f"{url}/{resource.strip()}"
        return url



def main(args=None):
    """Entry"""
    parser = argparse.ArgumentParser(prog="rct sh")
    parser.add_argument("-p", "--password", nargs="?", default="ess-pwe-f5site02")
    parser.add_argument("ip_address")
    options = parser.parse_args(args)

    if options.password is None:
        options.password = getpass.getpass("Password: ")

    # Tells readline that colon and dash are not a word delimiters
    delimiters = readline.get_completer_delims()
    delimiters = delimiters.replace(":", "").replace("-", "")
    readline.set_completer_delims(delimiters)

    # Load history
    history_path = pathlib.Path("~/.restconf_shell_history").expanduser()
    if history_path.exists():
        readline.read_history_file(history_path)

    try:
        shell = RestconfShell(options.ip_address, creds=("admin", options.password))
        shell.cmdloop()
    finally:
        readline.write_history_file(history_path)


if __name__ == "__main__":
    main()
