# Introduction

`cdfile` is a command-line tool I wrote to address one of my problems:
Within a development tree (i.e., a Perforce enlistment), I often need to
`cd` into a directory containing file *X*. Without `cdfile`, I would
have to carry the following tasks:

1. Use the Cygwin `find` command to find the file, which could take
   a couple of minutes

2. Once found, copy the path

3. `cd` to that path

With `cdfile`, the process is much more streamlined and faster. All I
have to do is typing the following command and I am there:

    cdfile filename

# Installation

Copy *cdfile.py* and *cdfile.cmd* to a directory in your path.

# Getting Started

Go to the top directory of your development tree (i.e. your
enlistment). Issue the following command

    cdfile any-file-name

After that, you can use `cdfile` from anywhere within your development
tree.

# How it Works

When `cdfile` starts, it looks for a hidden file called *.cdfile* in the
current directory. If not found, it will keep traversing up the directory
tree until it found one. If not found, `cdfile` will create the *.cdfile*
in the current directory. This hidden file is a database which stores
all the files and their locations. Currently, I use SQLite 3 format,
so you can view this file using the third-party `sqlite3` tool.

In theory, you can just go to the root directory (e.g. *C:\\*) and
generate the .cdfile database. However, you might not want to do that
and here is why. I currently have to development trees on *D:* drive:
*D:\\foo-dev* and *D:\\bar-dev*. They contain almost the same set of
files. With a single database at *D:\\.cdfile*, every time I issue the
command `cdfile myfile`, there will be duplicates and thus requiring me
to make a selection. The recommended usage is to generate the database
file from the top of each development tree

# Reset the Database

Currently, the only way to reset the database is to delete the .cdfile
database and issue the `cdfile` command from the top of the development
tree to re-generate it.

# Supported Platforms

I currently tested `cdfile` under Windows and not other platforms. I
have not tested `cdfile` with Python 3, only Python 2.7.
