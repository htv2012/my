"""
whatis: Windows only. Get version of a file
"""
import glob
import win32api
import sys


def get_filenames(wildcards):
    """
    Given a list of wild cards, return a list of file names
    """
    for wildcard in wildcards:
        for filename in glob.glob(wildcard):
            yield filename


def get_version_tuple(filename):
    """
    Given a file name, return the version tuple. If version information is not
    available, return a tuple of 4 zeros
    """
    try:
        info = win32api.GetFileVersionInfo(filename, '\\')
        version = (
            info['FileVersionMS'] >> 16,
            info['FileVersionMS'] & 0xffff,
            info['FileVersionLS'] >> 16,
            info['FileVersionLS'] & 0xffff,
        )
    except:
        version = ('0', '0', '0', '0')

    return version


def main():
    """
    Process all the file names and display the version information
    """
    for filename in get_filenames(sys.argv[1:]):
        version_tuple = get_version_tuple(filename)
        version_string = '.'.join(str(n) for n in version_tuple)
        print '%20s %s' % (version_string, filename)


if __name__ == '__main__':
    main()
