#!/usr/bin/env python
"""
Create a bean class from a set of properties

INPUT
class Server
String name
int port
boolean secured

OUTPUT
public class Server {
    String name;
    int port;
    boolean secured;

    public Server() {
        this.name = null;
        this.port = -1;
        this.secured = false;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    // Other properties here ...

}
"""
import argparse
import fileinput
import itertools
import pathlib
import re
import sys
from io import StringIO


MAIN_TEMPLATE = """
    public void start(String[] args) {{
    }}

    public static void main(String[] args) {{
        {class_name} app = new {class_name}();
        app.start(args);
    }}

"""

TOSTRING_PROLOGUE = '''
    public String toString() {
        return getClass().getSimpleName() + "{" '''

TOSTRING_EPILOGUE = '''            + "}";
        }
'''

TOSTRING_PROPERTY_TEMPLATE = '''            + "{property_name}=" + {getter}()'''


class Properties(argparse.Action):
    """
    Collect pairs of (type, property_name) from the command line
    arguments
    """
    def __call__(self, parser, namespace, values, option_string):
        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])
        getattr(namespace, self.dest).append(values)


def remove_prefix(name):
    """
    Remove the m_, s_ prefixes which are frequently used in Java naming
    """
    return re.sub(r'^[ms]_', '', name)


def make_method(prefix, property_name):
    """
    Given a prefix and the name of a property, construct the method name
    with proper camel case.
    """
    property_name = remove_prefix(property_name)
    return prefix + property_name[0].title() + property_name[1:]


def generate_main(class_name, class_file):
    """
    Generate start() and main()
    """
    class_file.write((MAIN_TEMPLATE.format(class_name=class_name)))


def generate_tostring(class_name, properties, class_file):
    """
    Generate toString()
    """
    def format_property(property_name):
        getter = make_method('get', property_name)
        formatted = TOSTRING_PROPERTY_TEMPLATE.format(property_name=property_name, getter=getter)
        return formatted

    class_file.write(TOSTRING_PROLOGUE)
    class_file.write('\n')
    class_file.write((' + ", "\n'.join(format_property(property_name) for _, property_name in properties)))
    class_file.write('\n')
    class_file.write(TOSTRING_EPILOGUE)
    class_file.write('\n')


def generate_class(class_name, properties, has_main, force):
    """
    Given a class name and a list of properties (type, name), generate
    Java class
    """
    class_filename = pathlib.Path('{}.java'.format(class_name))
    if class_filename.exists() and not force:
        print('File {} exists, will not overwrite, use -f flag to force'.format(class_filename))
        return 1

    with open(class_filename, 'w') as class_file:
        class_file.write('public class %s {\n' % class_name)

        # Default constructor
        class_file.write('    public %s() {}\n\n' % (class_name))

        for property_type, property_name in properties:
            class_file.write('    // Property: %s\n' % remove_prefix(property_name))
            class_file.write('    private %s %s;\n' % (property_type, property_name))

            class_file.write('    public %s %s() { return this.%s; }\n' % (
                property_type, make_method('get', property_name), property_name))
            class_file.write('    public void %s(%s value) { this.%s = value; }\n' % (
                make_method('set', property_name),
                property_type,
                property_name))
            class_file.write('    public %s %s(%s value) { %s(value); return this; }\n\n' % (
                class_name,
                make_method('with', property_name),
                property_type,
                make_method('set', property_name)))

        if has_main:
            generate_main(class_name, class_file)

        generate_tostring(class_name, properties, class_file)
        class_file.write('}\n\n')

        return 0

def parse_command_line_arguments():
    """
    Parse the command line arguments, including arguments stored in a
    file and return a namespace object with these arguments.
    """
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('-c', '--class', default='MyClass', dest='class_name')
    parser.add_argument('-p', '--property', nargs=2, action=Properties, dest='properties', default=[])
    parser.add_argument('-m', '--main', dest='has_main', action='store_true', default=False)
    parser.add_argument('-f', '--force', action='store_true', default=False, help='Force overwrite existing file')
    options = parser.parse_args()
    return options

def main():
    options = parse_command_line_arguments()
    return generate_class(options.class_name, options.properties, options.has_main, options.force)


if __name__ == '__main__':
    sys.exit(main())
