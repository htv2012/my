#!/usr/bin/env python3
"""
A tool to find files, then act on them
"""
import argparse
import itertools
import logging
import os
import platform
import sqlite3
import subprocess
import sys


DB_FILENAME = '.cdfile.sqlite'
DEFAULT_EXCLUDES = ['%.git%', '%__pycache__%', "%test-env%"]
logging.basicConfig(level=os.getenv('LOGLEVEL', logging.WARN))
LOGGER = logging.getLogger(__name__)

# TODO: Add sub parser to rescan

def get_paths_and_filenames(root):
    """
    Given a directory, return all paths/filenames pairs for all files
    """
    for dirpath, dirnames, filenames in os.walk(root):
        dirpath = os.path.abspath(dirpath)
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname), dirname
        for filename in filenames:
            yield dirpath, filename


def scan_dir(dirname, output_filename, excludes=None):
    """
    Scan the current directory for files and location
    """
    with sqlite3.connect(output_filename) as connection:
        connection.execute('DROP TABLE IF EXISTS locs')
        connection.execute('CREATE TABLE locs (loc text, fn text)')

        connection.executemany(
            'INSERT INTO locs VALUES (?, ?)',
            get_paths_and_filenames(dirname))

        for wildcard in excludes or []:
            wildcard = wildcard.replace('*', '%').replace('?', '_')
            connection.execute('DELETE FROM locs WHERE loc LIKE ?', (wildcard,))


def get_default_editor():
    """
    Search the environment variable for the default editor. If not
    found, then use vim
    """
    return os.getenv('EDITOR', 'vim')


def parse_command_line_arguments():
    """ Parse the command-line arguments """
    editor = get_default_editor()

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--exclude', action='append', default=DEFAULT_EXCLUDES)
    action = parser.add_subparsers(dest='action')
    action.required = True

    edit_action = action.add_parser('edit')
    edit_action.add_argument('-e', '--editor', default=editor)
    edit_action.add_argument('filenames', nargs='+')

    cd_action = action.add_parser('cd')
    cd_action.add_argument('-o', '--output', required=True, type=argparse.FileType('w'))
    cd_action.add_argument('filename')

    refresh_action = action.add_parser('refresh')

    arguments = parser.parse_args()
    return arguments


def locate_database(start_dir, filename):
    """
    Starting from a directory,traverse up the directory tree to find
    the database file
    """
    last_dir = ''
    while last_dir != start_dir:
        db_path = os.path.join(start_dir, filename)
        if os.path.exists(db_path):
            return db_path
        last_dir = start_dir
        start_dir = os.path.dirname(start_dir)
    return ''


def query_paths(db_path, wildcard):
    """
    Search the database for a list of entries which match the wildcard
    :param db_path: Path to the database file
    :param wildcard: The wildcard to search for, e.g. myfile*.py
    :returns: A list of paths
    """
    wildcard = wildcard.replace('*', '%').replace('?', '_')
    with sqlite3.connect(db_path) as connection:
        query = 'SELECT loc, fn FROM locs WHERE fn LIKE ? ORDER BY fn'
        rows = connection.execute(query, (wildcard,))

    rows = list(rows)
    LOGGER.debug('Rows:')
    for row in rows:
        LOGGER.debug('- %s', row)

    paths = [os.path.join(*row) for row in rows]
    return paths


def invoke_editor(editor, paths):
    """
    Invoke the editor on the list of paths

    :param editor: The name of the editor such as 'nano' or 'vim'
    :param paths: A list of paths to edit
    """
    LOGGER.debug('Invoke editor, editor=%r, paths=%r', editor, paths)
    command = [editor, '-p']
    print(' '.join(command), end=' ')
    print(' '.join('"{}"'.format(path) for path in paths))

    use_shell = 'Windows' in platform.system()
    subprocess.call(command + paths, shell=use_shell)


def search_and_edit(editor, filenames, db_path):
    """
    Searchs for files to edit, then invoke the editor on them

    :param editor: The name of the editor such as 'nano' or 'vim'
    :param filenames: A list of filenames to edit
    :param db_path: The file name of the database file
    :return: 0 if no error, 1 otherwise
    """
    destinations = []
    for filename in filenames:
        candidates = query_paths(db_path, filename)
        destination = choose_path(candidates)

        if destination is not None:
            destinations.append(destination)

    if not destinations:
        print('No file to edit')
        return 1

    invoke_editor(editor, destinations)
    return 0


def choose_path(candidates):
    """
    Given a list of candidates, ask the user to make a selection and
    return the selected directory
    """
    LOGGER.debug('choose_path, candidates=%r', candidates)
    if candidates == []:
        return None
    elif len(candidates) == 1:
        return candidates[0]

    for index, path in enumerate(candidates):
        print(f'{index:>2}. {path}')

    print('Please type a number to select location, or "q" to cancel')
    while True:
        choice = input('> ')
        if choice == 'q':
            return None

        try:
            choice = int(choice)
            return candidates[choice]
        except (ValueError, IndexError):
            pass


def write_output(output, destination):
    """
    Write the cd command to the output file. This function takes
    into consideration the current operating system (Windows, Linux,
    or Mac) and write out appropriate cd command for that OS.

    :param output: The output file handle
    :param destination: The destination directory
    """
    system = platform.system()
    if system == 'Darwin':
        system = 'Linux'

    prologue = dict(Windows='@echo off', Linux='#!/usr/bin/env bash')
    cd_command = dict(Windows='cd /d', Linux='cd')
    exit_command = dict(Windows='exit /b', Linux='return')
    exit_code = 0 if destination else 1

    output.write('{}\n'.format(prologue[system]))
    if destination is None:
        output.write('echo Cannot locate file\n')
    else:
        output.write('{} "{}"\n'.format(cd_command[system], destination))
        output.write('ls -l\n')
    output.write('{} {}'.format(exit_command[system], exit_code))


def create_cd_script(filename, output, db_path):
    """
    Creates a script to chdir to the directory where `filename`
    resides. Write the script to the file handle `output`.

    :param filename: The name of the file to cd into
    :param output: The file handle to write the output
    :param db_path: The database containing all files and paths
    :return: 0 if no error, 1 otherwise
    """
    LOGGER.debug("filename: %r", filename)
    candidates = query_paths(db_path, filename)
    destination = choose_path(candidates)
    LOGGER.debug("destination: %r", destination)
    if destination is not None:
        destination = os.path.dirname(destination)
    LOGGER.debug('Desitnation: %r', destination)
    write_output(output, destination)

    return 0 if destination is not None else 1

def main():
    """
    App entry point
    """
    arguments = parse_command_line_arguments()
    LOGGER.debug('Arguments: %r', arguments)

    db_path = locate_database(os.path.abspath('.'), DB_FILENAME)
    if db_path == '' or arguments.action == 'refresh':
        LOGGER.debug('Database not found, scan current dir')
        scan_dir('.', DB_FILENAME, arguments.exclude)
        db_path = locate_database(os.path.abspath('.'), DB_FILENAME)

    LOGGER.debug('db_path: %s', db_path)

    if arguments.action == 'edit':
        return search_and_edit(arguments.editor, arguments.filenames, db_path)
    elif arguments.action == 'cd':
        return create_cd_script(arguments.filename, arguments.output, db_path)

    return 0


if __name__ == '__main__':
    sys.exit(main())

