#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import argparse
import codecs
import json
import logging
import os
import platform
import subprocess
import sys


ALIAS_SECTION = 'aliases'
CDPATH_SECTION = 'cdpath'

try:
    ChdirError = WindowsError
except NameError:
    ChdirError = OSError


def get_local_config_dir():
    """
    Returns the configuration directory based on the platform. For
    Windows, it would be %LOCALAPPDATA%.
    """
    system = platform.system()
    if system == 'Windows':
        local_config_dir = os.getenv('LOCALAPPDATA')
    elif system.startswith('CYGWIN'):
        local_config_dir = os.getenv('LOCALAPPDATA')
        logger.debug('For cygwin, local config dir is %r', local_config_dir)
    else:
        raise NotImplementedError('Not yet implemented for %s' % system)

    return local_config_dir


def read_configurations(config_filename):
    """
    Read the configuration file and return a nested dictionary to
    represent the configuration. The dictionary has at least two keys:
    ALIAS_SECTION and CDPATH_SECTION
    """
    config = dict(cdpath=['.'], aliases=dict())
    try:
        with codecs.open(config_filename, 'r', encoding='utf-8') as f:
            lines = filter(lambda line: not line.strip().startswith('#'), f)
            contents = '\n'.join(lines)
            config = json.loads(contents)
    except IOError:
        pass

    config[ALIAS_SECTION]['-'] = os.getenv('OLDPWD', '.')
    return config


def list_configurations(config, config_filename):
    print(CDPATH_SECTION)
    for v in config[CDPATH_SECTION]:
        print('  {}'.format(v))

    print()
    print(ALIAS_SECTION)
    for k, v in sorted(config[ALIAS_SECTION].items()):
        print('  {}: {}'.format(k, v))

    print('\nconfig file:', config_filename)



def dos2cygwin_path(dos_path):
    dos_path = os.path.expandvars(dos_path)
    cygwin_path = subprocess.check_output(['cygpath.exe', dos_path])
    return cygwin_path.rstrip()


def generate_bash_script(config):
    for k, v in sorted(config[ALIAS_SECTION].items()):
        if k == '-':
            continue
        v = dos2cygwin_path(v)
        print('export {}={!r}'.format(k, v))


def expand_path(path):
    """
    Take a path and expand environment variables, interpret ~, ...
    """
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.normpath(path)
    return path


def search_cdpath(dirname, cdpath):
    """
    Given the name of a directory and a list of parent directories,
    find and return the absolute path. If not found, return None.
    """
    current_dir = os.getcwd().lower()
    found = []
    found_index = 0

    for parent_dir in cdpath:
        dest = expand_path(os.path.join(parent_dir, dirname))
        if os.path.exists(dest):
            found.append(dest)
        if current_dir == dest.lower():
            found_index = len(found)
            logger.debug('dest: %r, found_index: %r', dest, found_index)

    if not found:
        return None
    return found[found_index % len(found)]


def main():
    global logger
    log_level = os.environ.get('LOGLEVEL', logging.INFO)
    logging.basicConfig(level=log_level, format='%(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--bash',
        action='store_true',
        default=False,
        help='Generate bookmarks as bash variables')
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        default=False,
        help='List bookmarks')
    parser.add_argument(
        '-p',
        '--pushd',
        action='store_true',
        default=False,
        help='Generate command for pushd instead of cd')
    parser.add_argument(
        'dirname',
        nargs='?',
        type=expand_path,
        default='~',
        help='The destination directory')
    options = parser.parse_args()

    configuration_filename = os.path.join(
        get_local_config_dir(), 'southeastwind', 'nav.json')
    logger.debug('Configuration file: %s', configuration_filename)
    config = read_configurations(configuration_filename)

    if options.list:
        list_configurations(config, configuration_filename)
        return 0
    elif options.bash:
        generate_bash_script(config)
        return 1

    # Determine the directory
    dest = config[ALIAS_SECTION].get(options.dirname) or \
        search_cdpath(options.dirname, config[CDPATH_SECTION])

    if dest is None:
        print('Dir not found:', options.dirname)
        return 1

    # Attempt to chdir to verify the dir existence and get the absolute name
    current_dir = os.getcwd()
    try:
        dest = expand_path(dest)
        os.chdir(dest)
        dest = os.getcwd()
    except ChdirError as exception_info:
        logger.debug('Exception:\n %s', exception_info)
        print('Cannot locate dir:', options.dirname)
        return 1

    logger.debug('dirname = %s', dest)

    cd_command = 'chdir /d' if platform.system() == 'Windows' else 'cd'
    if options.pushd:
        cd_command = 'pushd'

    print('set OLDPWD=%s' % current_dir)
    print('%s "%s"' % (cd_command, dest))

    return 0


if __name__ == '__main__':
    sys.exit(main())
