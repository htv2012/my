#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import json
import logging
import marshal
import os
import subprocess
import sys


class PerforceError(BaseException):
    pass


logging.basicConfig(level=os.getenv('LOGLEVEL', 'WARN'))
logger = logging.getLogger(__name__)


def byte2str_dict(dict_object):
    """
    Given a dictionary, convert all of its keys and values from bytes
    to unicode strings.

    This function does not recurse if value itself is a dictionary.
    """
    if sys.version_info.major < 3:
        return dict_object

    logger.debug('dict before: %r', dict_object)

    dict_object = {
        k.decode('utf-8'):
        v.decode('utf-8') if isinstance(v, bytes) else v
            for k, v in dict_object.items()
    }

    logger.debug('dict after: %r', dict_object)
    return dict_object


def execute_perforce_command(*args):
    """
    Run a perforce command an return one or more JSON objects
    representing the output. That means the output could be a single
    dictionary or a list of dictionaries
    """
    command = ['p4', '-G'] + list(args)
    process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    dict_objects = []
    try:
        while True:
            dict_object = marshal.load(process.stdout)

            # Python 2 vs 3: In python 2, str and bytes are
            # interchangeable. However in Python 3, the process.stdout
            # returns a bytes stream, thus the dict_object's keys
            # and values are also bytes. We need to conver them to
            # unicode or json.dumps() will choke.
            dict_object = byte2str_dict(dict_object)
            dict_objects.append(dict_object)
    except EOFError:
        pass

    for dict_object in dict_objects:
        if dict_object.get('code') == 'error':
            logger.debug('Command: %r', args)
            logger.debug('dict_objects: %r', dict_objects)
            raise PerforceError(dict_object['data'])

    if len(dict_objects) == 1:
        dict_objects = dict_objects[0]

    return dict_objects


def main():
    """
    Run a perforce command and display the output in JSON format
    """
    try:
        dict_objects = execute_perforce_command(*sys.argv[1:])
    except PerforceError as exception:
        print(exception)
        return 1

    print(json.dumps(dict_objects, indent=4, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
