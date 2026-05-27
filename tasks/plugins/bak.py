import pathlib

from fabric import Connection, task

from tools import banner

@task
def ls(c: Connection):
    c.run("ls -lh ~/Arc")

@task
def foo(c: Connection):
    pass