#!/usr/bin/env python
"""
Create a new Java project here
"""
from __future__ import print_function
import argparse
import os
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('class_name')
    options = parser.parse_args()
    class_name = options.class_name

    # Make directory
    os.mkdir(class_name)
    os.chdir(class_name)

    # Create files and directory structure
    archive_filename = os.path.splitext(__file__)[0] + '.zip'
    archive = zipfile.ZipFile(archive_filename)
    archive.extractall()

    # Rename the main module
    java_module_filename = 'src/main/java/{}.java'.format(class_name)
    os.rename('src/main/java/HelloWorld.java', java_module_filename)

    # Fix up the class name
    with open(java_module_filename, 'r') as f:
        contents = f.read().replace('HelloWorld', class_name)
    with open(java_module_filename, 'w') as f:
        f.write(contents)

    print('Project created, to get started:')
    print('cd', class_name)
    print('source source_me.sh')
    print('run')


if __name__ == '__main__':
    main()
