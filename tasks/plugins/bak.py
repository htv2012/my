from fabric import Connection, task


@task
def ls(c: Connection):
    c.run("ls -lh ~/Arc")


@task
def foo(c: Connection):
    pass
