#!/usr/bin/env python
"""
Create a new java source
"""
from __future__ import print_function
import argparse
import os
import subprocess


IMPORTS = """
import java.io.*; // File, IOException

import java.nio.file.attribute.BasicFileAttributes;

// DirectoryStream, Files, FileSystem, FileVisitOption
// NoSuchFileException, Path, PathMatcher, Paths, SimpleFileVisitor
import java.nio.file.*;

// Arrays, HashSet, List, Optional
import java.util.*;

// Stream
import java.util.stream.*;

"""

CLASS_TEMPLATE = """public class {class_name} {{
    public void start(String[] args) {{
    }}

    public static void main(String[] args) {{
        {class_name} app = new {class_name}();
        app.start(args);
    }}
}}
"""


def parse_command_line_arguments():
    """
    Parse the command line arguments, including arguments stored in a
    file and return a namespace object with these arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', default=False, action='store_true')
    parser.add_argument('-e', '--edit', default=False, action='store_true')
    parser.add_argument('class_name')
    options = parser.parse_args()
    return options


def main():
    options = parse_command_line_arguments()
    class_name = options.class_name

    filename = class_name + ".java"
    if os.path.exists(filename) and not options.force:
        print('File %s exists, to override, use the -f flag' % filename)
        return 1

    try:
        with open(filename, 'w') as source_file:
            source_file.write(IMPORTS)
            source = CLASS_TEMPLATE.format(class_name=class_name)
            source_file.write(source)
            if options.edit:
                command = ['code', filename]
                subprocess.check_call(command)
    except Exception as exception:
        print('Error: %s' % exception)
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
