#!/usr/bin/env python3
"""
Manages ~/.ssh/config file
"""

from __future__ import print_function

import argparse
import logging
import os
import platform
from fnmatch import fnmatch

# pylint: disable=redefined-builtin
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError
# pylint: enable=redefined-builtin


logging.basicConfig(level=os.getenv("LOGLEVEL", "WARN"))
LOGGER = logging.getLogger(__name__)


COMMAND_LIST = "ls"
COMMAND_REMOVE = "rm"
COMMAND_UPDATE = "update"


def get_config_filename():
    """
    Return the ssh config filename for the current host
    """
    if platform.system() == "Windows":
        username = os.getenv("USERNAME")
        home = os.getenv("HOME", "C:\\cygwin\\home\\" + username)
        config_filename = os.path.join(home, ".ssh", "config")
    else:
        config_filename = os.path.expanduser("~/.ssh/config")

    return config_filename


def filter_keys_by_wildcard(dictobject, wildcard):
    """
    Given a dictionary and a wildcard, return those items whose keys
    match the wildcard
    """
    return sorted((k, v) for k, v in dictobject.items() if fnmatch(k, wildcard))


def config_read(filename=None):
    """
    Read configuration from a file, default is ~/.ssh/config.
    """
    filename = filename or get_config_filename()
    with open(filename) as file_handle:
        config = {}
        for line in file_handle:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            try:
                key, value = line.split("=", 1)
            except ValueError:
                key, value = line.split(" ", 1)

            if key == "Host":
                host = value
                config.setdefault(host, {})
            else:
                config[host][key] = value

        return config


def config_save(config, filename=None):
    """
    Save the config to a file, default is ~/.ssh/config.
    """
    filename = filename or get_config_filename()
    with open(filename, "w") as file_handle:
        config_write(config, file_handle, wildcard="*")


def config_write(config, file_handle, wildcard):
    """
    Write the config to a file handle
    """
    for host, host_info in sorted(config.items()):
        if not fnmatch(host, wildcard):
            continue

        file_handle.write("Host {}\n".format(host))
        for key, value in sorted(host_info.items()):
            file_handle.write("    {} {}\n".format(key, value))
        file_handle.write("\n")


def config_list(config, wildcard, verbose):
    """
    Print to console the list of hosts
    """
    hosts = filter_keys_by_wildcard(config, wildcard)
    for host, host_info in hosts:
        print("{}: {}".format(host, host_info["HostName"]))
        if verbose:
            del host_info["HostName"]
            for key, value in host_info.items():
                print("    {}: {}".format(key, value))


def update(config, host, **kwargs):
    """
    Update a host information. Some notable kwargs keys are HostName,
    User, IdentityFile, ForwardX11, and FowardX11Trusted.

    :param host: The host name
    :param kwargs: The keys/values applicable to ~/.ssh/config
    """

    host_config = config.setdefault(host, {})
    host_config.update(kwargs)


def parse_command_line():
    """
    Parse command line and return the arguments

    :return: A argparse.Namespace object containing the parsed information
    """
    parser = argparse.ArgumentParser()
    actions = parser.add_subparsers(dest="command", required=True)

    list_action = actions.add_parser("ls")
    list_action.add_argument("-v", "--verbose", default=False, action="store_true")
    list_action.add_argument("wildcard", nargs="?", default="*")

    remove_action = actions.add_parser(COMMAND_REMOVE)
    remove_action.add_argument("hosts", nargs="+")

    update_action = actions.add_parser(COMMAND_UPDATE)
    update_action.add_argument("host")
    update_action.add_argument("keyvalues", nargs="+")

    args = parser.parse_args()
    LOGGER.debug("args=%s", args)
    return args


def main():
    """Entry point"""
    args = parse_command_line()

    try:
        config = config_read()
    except FileNotFoundError as exc:
        print(exc)
        raise SystemExit(1)

    if args.command == COMMAND_LIST:
        config_list(config, args.wildcard, args.verbose)
    elif args.command == COMMAND_UPDATE:
        new_kv = dict(e.split("=") for e in args.keyvalues)
        update(config, args.host, **new_kv)
        config_save(config)
    elif args.command == COMMAND_REMOVE:
        for host in args.hosts:
            config.pop(host, None)
            config_save(config)


if __name__ == "__main__":
    main()
